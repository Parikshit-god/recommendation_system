import pandas as pd
import ast

print("Step 1: Loading data...")
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

print("Step 2: Merging data...")
# We combine both files based on the movie title
movies = movies.merge(credits, on='title')

print("Step 3: Selecting important columns...")
# We only keep what we need for recommendations
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

print("Step 4: Cleaning data and extracting names...")
# Remove any movies that are missing an overview or other data
movies.dropna(inplace=True)

# Helper function to extract names (like "Action" or "Adventure") from the weird format
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

# Helper function to get only the top 3 actors
def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

# Helper function to find the Director's name
def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

# Apply our helper functions to the columns
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

print("Step 5: Removing spaces to make unique tags...")
# We remove spaces so "Science Fiction" becomes "ScienceFiction". 
# This stops the engine from confusing "Johnny Depp" and "Johnny Galecki" because of the word "Johnny".
def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ", ""))
    return L1

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

print("Step 6: Processing overview and combining into 'tags'...")
# Split the overview paragraph into single words
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Add all these lists together into one big column called 'tags'
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

print("Step 7: Creating the final dataset...")
# Make a clean dataframe with just ID, Title, and Tags
new_df = movies[['movie_id', 'title', 'tags']].copy()

# Join the list of tags back into a single sentence separated by spaces
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
# Make everything lowercase so the engine doesn't treat "Action" and "action" differently
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

print("Step 8: Saving cleaned data...")
# Save this new clean data to a new CSV file
new_df.to_csv('cleaned_movies.csv', index=False)
print("SUCCESS! Cleaned data saved as 'cleaned_movies.csv'.")