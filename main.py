import os
import uuid
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import sys_msg

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# System message for the chatbot
system_message = sys_msg.system_message

# Ensure the system message exists in history at initialization
history = [{"role": "system", "content": system_message}]

# Path to store speech files
speech_dir = Path(__file__).parent / "speech_files"
speech_dir.mkdir(exist_ok=True)


# Function to generate audio from text using OpenAI TTS
def text_to_speech(text, output_filename=None):
    """
    Converts text to speech using OpenAI's TTS model and saves it to a file.
    Args:
        text (str): The text to convert to speech.
        output_filename (str): The name of the output file.
    Returns:
        str: The filename of the generated speech file.
    """
    if output_filename is None:
        output_filename = f"speech_{uuid.uuid4().hex}.mp3"  # Unique filename

    speech_file_path = speech_dir / output_filename
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file(speech_file_path)
    print(f"Audio saved to {speech_file_path}")
    return output_filename


# Function to validate the conversation history
def validate_history(history):
    """
    Ensures that all entries in the history list have the required 'role' and 'content' keys.
    Args:
        history (list): The conversation history for the OpenAI API.
    """
    for msg in history:
        if "role" not in msg or "content" not in msg:
            raise ValueError(f"Malformed API history entry: {msg}")


# Function to generate chatbot responses
def chat_with_bot(user_input, chat_history):
    """
    Generates a chatbot response based on user input and updates the conversation history.
    Args:
        user_input (str): The user's input message.
        chat_history (list): The conversation history for the frontend.
    Returns:
        tuple: The assistant's reply and the updated chat_history.
    """
    # Maintain a separate history for OpenAI API
    api_history = [{"role": "system", "content": sys_msg.system_message}]
    for entry in chat_history:
        if "user" in entry:
            api_history.append({"role": "user", "content": entry["user"]})
        if "bot" in entry:
            api_history.append({"role": "assistant", "content": entry["bot"]})

    # Append the new user input to the API history
    api_history.append({"role": "user", "content": user_input})

    # Debugging the history structure before API call
    print("API History:", api_history)

    # Validate the API history
    validate_history(api_history)

    # Generate a response from the assistant
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=api_history,
        max_tokens=200,
    )
    assistant_reply = response.choices[0].message.content

    # Append the user and bot messages to the frontend chat history
    chat_history.append({
        "user": user_input,
        "bot": assistant_reply,
        "audio": None  # Placeholder for audio file, added later
    })

    return assistant_reply, chat_history
