from flask import Flask, render_template, request
from main import chat_with_bot, history  # Import functions and conversation history from main.py

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    bot_reply = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_reply, _ = chat_with_bot(user_input, history)  # Call the chat function from main.py
    return render_template("chat.html", bot_reply=bot_reply)

if __name__ == "__main__":
    app.run(debug=True)
