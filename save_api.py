import json
import os
import time
import requests
# File path for storing the cached data
CACHE_FILE = "static/movie_and_poster_cache.json"

def save_to_json_file(data, filepath):
    """Save data to a JSON file (overwrites existing content)."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_from_json_file(file_path):
    """Load data from a JSON file if it exists."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None

def fetch_movie_and_poster(filepath):
    """Fetch movie and poster data, and save it to a JSON file."""
    # Fetch most popular movies
    popular_movies = fetch_most_popular_movies()

    # Add movie poster URLs and ratings
    for movie in popular_movies:
        movie_id = movie['id']
        movie['image'] = fetch_movie_poster(movie_id)
        if movie.get('averageRating') is not None:
            movie['averageRating'] = str(movie['averageRating']) + "⭐"
        else:
            movie['averageRating'] = "N/A ⭐"
        time.sleep(1)  # Avoid hitting API rate limits

    # Save new data to the file (overwrites existing content)
    save_to_json_file(popular_movies, filepath)
    print(f"Data successfully saved to {filepath}.")

def fetch_most_popular_movies():
    url = "https://imdb236.p.rapidapi.com/imdb/most-popular-movies"
    headers = {
        "X-RapidAPI-Key": "c972f43f32msh51e91b74431ac9bp1f5267jsn80988ac834d1",  # Replace with your API key
        "X-RapidAPI-Host": "imdb236.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the top 10 movies
        top_10_movies = [
            movie
            for movie in data[:10]  # Access directly since it's a list
        ]
        return top_10_movies
    else:
        print("Failed to fetch most popular movies:", response.status_code, response.text)
        return []
    
def fetch_movie_poster(movie_id):
    # Correct API endpoint for movie details
    url = f"https://imdb-com.p.rapidapi.com/title/get-taglines?tconst={movie_id}"

    headers = {
        "X-RapidAPI-Key": "c972f43f32msh51e91b74431ac9bp1f5267jsn80988ac834d1",
        "X-RapidAPI-Host": "imdb-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Extract the image URL
        image_url = data['data']['title']['primaryImage']['url']  
        return image_url
    else:
        print(f"Failed to fetch poster for {movie_id}:", response.status_code, response.text)
        return None

def fetch_movie_description(movie_id):
    url = f"https://mdblist.p.rapidapi.com/?i={movie_id}"  # Replace with the actual endpoint
    headers = {
        "X-RapidAPI-Key": "c972f43f32msh51e91b74431ac9bp1f5267jsn80988ac834d1",  # Replace with your RapidAPI key
        "X-RapidAPI-Host": "mdblist.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['description']
        # Extract and return the description
        
    else:
        print(f"Failed to fetch movie details: {response.status_code}")
        return None



top_10 = fetch_most_popular_movies()
extracted_movies = [{key: movie[key] for key in ['primaryTitle', 'genres', 'startYear', 'id', 'averageRating']} for movie in top_10 ]
for movie in extracted_movies:
    movie['description'] = fetch_movie_description(movie['id'])
    time.sleep(1)
save_to_json_file(extracted_movies, 'static/trending_movies_cache_for_sysmsg.json')