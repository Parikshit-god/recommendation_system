import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

print("Step 1: Loading the cleaned data...")
# Load the CSV we made in Phase 3
movies_df = pd.read_csv('cleaned_movies.csv')

# Safety check: replace any blank tags with an empty string so the math doesn't break
movies_df['tags'] = movies_df['tags'].fillna('')

print("Step 2: Converting text into numbers (Vectorization)...")
# We take the top 5000 most common words, ignoring common English words like 'and', 'the', 'is'
cv = CountVectorizer(max_features=5000, stop_words='english')

# Convert the 'tags' column into a mathematical matrix
vectors = cv.fit_transform(movies_df['tags']).toarray()

print("Step 3: Calculating movie similarities...")
# Calculate how similar every movie is to every other movie
similarity = cosine_similarity(vectors)

print("Step 4: Saving the model files...")
# We use 'pickle' to save our data and our math results into files we can load instantly later
# 'wb' means "write binary"
pickle.dump(movies_df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("SUCCESS! 'movies.pkl' and 'similarity.pkl' have been saved to your folder.")