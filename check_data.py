import pandas as pd

print("Loading datasets...")

try:
    # Load the movies dataset
    movies = pd.read_csv("tmdb_5000_movies.csv")
    print("Successfully loaded movies data!")
    print(f"Total movies: {len(movies)}")

    # Load the credits dataset
    credits = pd.read_csv("tmdb_5000_credits.csv")
    print("Successfully loaded credits data!")
    print(f"Total credits: {len(credits)}")

    print("\nEverything is working perfectly! You are ready for Phase 3.")

except FileNotFoundError as e:
    print("\nERROR: Could not find the CSV files.")
    print("Please make sure 'tmdb_5000_movies.csv' and 'tmdb_5000_credits.csv'")
    print("are exactly inside your 'recommendation-system' folder.")