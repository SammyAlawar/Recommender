from flask import Flask, render_template, request, send_from_directory
from main import chat_with_bot, text_to_speech
from pathlib import Path
import uuid
import sys_msg
import json

app = Flask(__name__)

# Directory to save generated speech files
speech_dir = Path(__file__).parent / "speech_files"
speech_dir.mkdir(exist_ok=True)

# Initialize chat history
chat_history = []

from flask import jsonify

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history
    bot_reply = None
    audio_filename = None

    # Fetch the top 10 movies
    with open("static/movie_and_poster_cache.json", "r") as f:
        popular_movies = json.load(f)

    if request.method == "POST":
        # Get user input and language selection
        user_input = request.form["user_input"]
        selected_language = request.form["language"]

        # Choose the system message based on the language
        if selected_language == "ar":
            system_message = sys_msg.system_message_ar
        else:
            system_message = sys_msg.system_message

        

        # Get bot response
        bot_reply, chat_history = chat_with_bot(user_input, chat_history, system_message)

        # Generate unique audio file for the bot reply
        audio_filename = text_to_speech(bot_reply)
        chat_history[-1]["audio"] = audio_filename  # Update the last bot entry with audio file

        # Return the bot's reply and audio filename as a JSON response
        return jsonify({"bot_reply": bot_reply, "audio_filename": audio_filename})

    # For GET requests, render the chat history page
    return render_template("chat.html", chat_history=chat_history, popular_movies=popular_movies)




# Route to serve the audio files
@app.route("/speech/<filename>")
def serve_audio(filename):
    return send_from_directory(speech_dir, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
