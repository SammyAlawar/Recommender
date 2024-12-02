from flask import Flask, render_template, request, send_from_directory
from main import chat_with_bot, text_to_speech
from pathlib import Path
import uuid

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

    if request.method == "POST":
        # Get user input
        user_input = request.form["user_input"]

        # Get bot response
        bot_reply, chat_history = chat_with_bot(user_input, chat_history)

        # Generate unique audio file for the bot reply
        audio_filename = text_to_speech(bot_reply)
        chat_history[-1]["audio"] = audio_filename  # Update the last bot entry with audio file

        # Return the bot's reply and audio filename as a JSON response
        return jsonify({"bot_reply": bot_reply, "audio_filename": audio_filename})

    # For GET requests, render the chat history page
    return render_template("chat.html", chat_history=chat_history)



# Route to serve the audio files
@app.route("/speech/<filename>")
def serve_audio(filename):
    return send_from_directory(speech_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
