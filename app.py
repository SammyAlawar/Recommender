from flask import Flask, render_template, request, send_from_directory, session
from main import chat_with_bot, text_to_speech
from main import chat_with_bot, text_to_speech ,  censor_inappropriate_words, load_inappropriate_words
from pathlib import Path
import sys_msg
import json
import random
app = Flask(__name__)

import secrets
app.secret_key = secrets.token_hex(16)
QUIZ_MOVIES_JSON = Path(__file__).parent / "static/quiz_movies.json"

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

        censored_input = censor_inappropriate_words(user_input, load_inappropriate_words('inappropriate_words.csv', selected_language))
        # Log censored input
        print(f"Censored User Input: {censored_input}")

        # Choose the system message based on the language
        if selected_language == "ar":
            system_message = sys_msg.system_message_ar
        else:
            system_message = sys_msg.system_message

        

        # Get bot response
        bot_reply, chat_history = chat_with_bot(censored_input, chat_history, system_message)

        # Generate unique audio file for the bot reply
        audio_filename = text_to_speech(bot_reply)
        chat_history[-1]["audio"] = audio_filename  # Update the last bot entry with audio file

        # Return the bot's reply and audio filename as a JSON response
        return jsonify({"bot_reply": bot_reply, "audio_filename": audio_filename})

    # For GET requests, render the chat history page
    return render_template("chat.html", chat_history=chat_history, popular_movies=popular_movies)

@app.route("/load_inappropriate_words")
def load_inappropriate_words_route():
    language = request.args.get("language", "en")  # Default to "en" if no language is provided
    inappropriate_words = load_inappropriate_words('inappropriate_words.csv', language)

    return jsonify({"words": inappropriate_words})


@app.route("/quiz", methods=["GET"])
def quiz():
    print(f"QUIZ_MOVIES_JSON Path: {QUIZ_MOVIES_JSON}")
    
    # Load movies from JSON
    with open(QUIZ_MOVIES_JSON, "r") as f:
        try:
            movies = json.load(f)  # Load the JSON file
            print(f"Type of movies: {type(movies)}")  # Debugging: Should be <class 'list'>
            print(f"First 5 movies: {movies[:5]}")    # Debugging: Check content
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return "Error loading quiz data", 500

    # Validate movies
    if not isinstance(movies, list):
        return "Invalid data format: movies data is not a list.", 400

    # Randomly select 5 movies
    if len(movies) < 5:
        return "Not enough movies in the file for the quiz", 400

    quiz_movies = random.sample(movies, 5)  # Select 5 random movies
    print("Selected movies:", quiz_movies)  # Debugging: Check selected movies

    # Save to session
    session["quiz_movies"] = quiz_movies
    session["responses"] = []

    # Serve the first movie
    return render_template("quiz.html", movie=quiz_movies[0], index=0)



@app.route("/quiz/response", methods=["POST"])
def quiz_response():
    # Get the response and index from the request
    data = request.json
    liked = data.get("liked")
    index = data.get("index")

    # Retrieve movies and responses from the session
    quiz_movies = session.get("quiz_movies", [])
    responses = session.get("responses", [])

    # Save the response for the current movie
    if index < len(quiz_movies):
        movie = quiz_movies[index]
        responses.append({"movie": movie, "liked": liked})
        session["responses"] = responses

    # Check if there are more movies to display
    if index + 1 < len(quiz_movies):
        next_movie = quiz_movies[index + 1]
        return jsonify({"movie": next_movie, "index": index + 1})
    else:
        # Calculate the user's preferred genre
        liked_movies = [resp["movie"] for resp in responses if resp["liked"]]
        genre_count = {}
        for movie in liked_movies:
            for genre in movie.get("genres", []):
                genre_count[genre] = genre_count.get(genre, 0) + 1

        # Find the most common genre
        favorite_genre = max(genre_count, key=genre_count.get, default="Unknown")

        # Save the favorite genre in the session
        session["favorite_genre"] = favorite_genre

        # Return the result box content
        return jsonify({
            "finished": True,
            "result_box": f"You seem to enjoy movies in the {favorite_genre} genre. Share this with the chatbox for personalized recommendations!",
        })

# Route to serve the audio files
@app.route("/speech/<filename>")
def serve_audio(filename):
    return send_from_directory(speech_dir, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
