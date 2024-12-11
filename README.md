# Cinema AI: Mood-Based Movie Recommendation Chatbot

## Overview
Cinema AI is a chatbot designed to recommend movies based on user emotions and preferences. Using advanced natural language processing (NLP) and real-time movie data, the chatbot provides highly personalized movie suggestions, saving users the hassle of endlessly scrolling through streaming platforms.

---

## Features
1. *Mood-Based Recommendations*
   - Leverages a fine-tuned DistilBERT model to analyze user input and identify emotions.
   - Recommends movies aligned with emotions such as happiness, sadness, or excitement.

2. *Movie Data Integration*
   - Fetches top trending movies from IMDb APIs.
   - Provides movie details like posters, genres, ratings, and descriptions.

3. *Speech-to-Text (STT) and Text-to-Speech (TTS)*
   - Allows users to input queries using voice commands.
   - Converts chatbot responses into audio for enhanced accessibility.

4. *Interactive Movie Quiz*
   - Calculates favorite genres based on responses for personalized recommendations.

5. *Multilingual Support*
   - Supports both English and Arabic for diverse user needs.

6. *Inappropriate words censoring*
   - Ensures a respectful user experience using a filtering system.
---

## How to Run the Application

### Prerequisites
- Python 3.9+ (for manual execution).


### Running Locally on Mac
1. Clone the repository:
   bash
   git clone https://github.com/SammyAlawar/Recommender.git
   cd Recommender
   

2. Create a virtual environment and activate it:
   bash
   python3 -m venv venv
   source venv/bin/activate 
   

3. Install dependencies:
   bash
   venv/bin/python3.9 -m pip install -r requirements.txt
   
4. Install the fine-tuned model:
     https://drive.google.com/drive/folders/1x0wKNL8-Aa6pFdkhXxhyr_voHUgR8gX4
     
5. Run the Flask application:
   bash
   venv/bin/python3.9 app.py
   

6. Access the application in your browser at:
   
   http://localhost:5000
   


   ### Running Locally on Windows
1. Clone the repository:
   
   git clone https://github.com/SammyAlawar/Recommender.git
   cd Recommender
   

2. Create a virtual environment and activate it:
   bash
   \Path\To\Python\Python39\python.exe -m venv venv 
   

3. Install dependencies:
   bash
  venv\Scripts\python.exe -m pip install -r requirements.txt
  
4. Install the fine-tuned model:
     https://drive.google.com/drive/folders/1x0wKNL8-Aa6pFdkhXxhyr_voHUgR8gX4
     
5. Run the Flask application:
   bash
   venv\Scripts\python.exe app.py
   

6. Access the application in your browser at:
   
   http://localhost:5000
   
---

## Future Enhancements
1. *Integration with Streaming Platforms*
   - Directly link users to movies on services like Netflix or Amazon Prime.

2. *Multilingual Expansion*
   - Support additional languages beyond English and Arabic.

3. *AI-Driven Watchlists*
   - Create personalized watchlists based on user interaction.

4. *Voice Command Navigation*
   - Enable hands-free operation for a seamless experience.
