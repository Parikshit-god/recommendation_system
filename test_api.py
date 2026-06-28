# test_api.py
import requests
from config import TMDB_API_KEY

def fetch_poster_test():
    print("Testing TMDB API connection...")
    
    # We are testing with movie ID 550, which is the movie "Fight Club"
    movie_id = 550 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    
    try:
        # Ask the waiter (API) for the data
        response = requests.get(url)
        data = response.json()
        
        # Check if we got a poster path back
        if 'poster_path' in data:
            poster_url = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            print("\nSUCCESS! Your API key works perfectly.")
            print(f"Movie Title: {data.get('title')}")
            print(f"Poster URL: {poster_url}")
            print("\n(You can copy and paste that Poster URL into your browser to see the image!)")
        else:
            print("\nERROR: The API key worked, but we couldn't find a poster.")
            print("Data received:", data)
            
    except Exception as e:
        print("\nERROR: Something went wrong trying to connect to TMDB.")
        print("Error details:", e)

# Run the test
fetch_poster_test()