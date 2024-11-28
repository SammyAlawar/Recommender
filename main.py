import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import sys_msg

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

system_message = sys_msg.system_message
history = [{"role": "system", "content": system_message}]

# Path to store speech files
speech_dir = Path(__file__).parent / "speech_files"
speech_dir.mkdir(exist_ok=True)

# Function to generate audio from text using OpenAI TTS
def text_to_speech(text, output_filename="speech.mp3"):
    speech_file_path = speech_dir / output_filename
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file(speech_file_path)
    print(f"Audio saved to {speech_file_path}")

# Function to generate chatbot responses
def chat_with_bot(user_input, history):
    history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        max_tokens=200
    )
    assistant_reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply, history

# Voice-enabled chatbot interaction
if __name__ == "__main__":
    print("Welcome to the Entertainment Recommender Bot!")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Bot: Goodbye! Have a great day!")
            break
        
        bot_reply, history = chat_with_bot(user_input, history)
        print(f"Bot: {bot_reply}")
        text_to_speech(bot_reply, output_filename="bot_reply.mp3")
