from flask import Flask, render_template, request, send_from_directory
from main import chat_with_bot, history, text_to_speech
from pathlib import Path

app = Flask(__name__)

# Directory to save generated speech files
speech_dir = Path(__file__).parent / "speech_files"
speech_dir.mkdir(exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    bot_reply = None
    audio_filename = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_reply, _ = chat_with_bot(user_input, history)
        
        # Generate speech for the bot's reply
        audio_filename = "bot_reply.mp3"
        text_to_speech(bot_reply, audio_filename)

    return render_template("chat.html", bot_reply=bot_reply, audio_filename=audio_filename)

# Route to serve the audio file
@app.route("/speech/<filename>")
def serve_audio(filename):
    return send_from_directory(speech_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
