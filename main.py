import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import sys_msg

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

system_message = sys_msg.system_message

history = [{"role": "system", "content": system_message}]

#Function to generate response 
def chat_with_bot(user_input, history):
    history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = history,
        max_tokens = 200 
    )

    assistant_reply = response.choices[0].message.content
        
    # Append the assistant's reply to the conversation history
    history.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply, history

    
# Simulate a real-time app
if __name__ == "__main__":
    print("Welcome to the Entertainment Recommender Bot!")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Bot: Goodbye! Have a great day!")
            break
        
        # Get the bot's response
        bot_reply, history = chat_with_bot(user_input, history)
        print(f"Bot: {bot_reply}")