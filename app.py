import streamlit as st
import pickle
import pandas as pd
import requests
import time
from config import TMDB_API_KEY

st.set_page_config(page_title="Movie Recommender", layout="wide", page_icon="🍿")

# --- THE APP'S MEMORY ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

network_session = requests.Session()
network_session.headers.update({'User-Agent': 'Mozilla/5.0'})

# --- HELPER FUNCTIONS ---

def fetch_poster_only(movie_id):
    """Fetches just the poster for the main page recommendations."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    for attempt in range(3):
        try:
            response = network_session.get(url, timeout=5).json()
            if 'poster_path' in response and response['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + response['poster_path']
            return "https://dummyimage.com/500x750/cccccc/000000.png&text=No+Poster"
        except:
            time.sleep(1)
    return "https://dummyimage.com/500x750/cccccc/000000.png&text=Error"

def fetch_full_details(movie_id):
    """Fetches plot, cast, ratings, revenue, and where to watch in ONE massive request."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits,reviews,watch/providers"
    
    # FIXED: We added the 3-try loop here so it doesn't fail on a tiny network drop!
    for attempt in range(3):
        try:
            data = network_session.get(url, timeout=5).json()
            
            # Check if TMDB explicitly rejected us
            if 'success' in data and data['success'] == False:
                print(f"TMDB API Error on movie {movie_id}: {data.get('status_message')}")
                return None
            
            details = {
                'title': data.get('title', 'Unknown Title'),
                'overview': data.get('overview', 'No plot summary available.'),
                'rating': round(data.get('vote_average', 0), 1),
                'release_date': data.get('release_date', 'Unknown'),
                'revenue': data.get('revenue', 0),
                'poster': "https://dummyimage.com/500x750/cccccc/000000.png&text=No+Poster"
            }
            
            if data.get('poster_path'):
                details['poster'] = "https://image.tmdb.org/t/p/w500/" + data.get('poster_path')
                
            cast = []
            if 'credits' in data and 'cast' in data['credits']:
                for actor in data['credits']['cast'][:5]:
                    pic = "https://dummyimage.com/200x300/cccccc/000000.png&text=No+Photo"
                    if actor.get('profile_path'):
                        pic = "https://image.tmdb.org/t/p/w200/" + actor['profile_path']
                    cast.append({'name': actor['name'], 'character': actor['character'], 'pic': pic})
            details['cast'] = cast
            
            reviews = []
            if 'reviews' in data and 'results' in data['reviews']:
                for rev in data['reviews']['results'][:2]:
                    reviews.append({'author': rev['author'], 'content': rev['content'][:400] + "..."})
            details['reviews'] = reviews
            
            details['watch_link'] = None
            if 'watch/providers' in data and 'results' in data['watch/providers']:
                providers = data['watch/providers']['results']
                if 'US' in providers and 'link' in providers['US']:
                    details['watch_link'] = providers['US']['link']
                elif providers:
                    first_country = list(providers.keys())[0]
                    details['watch_link'] = providers[first_country].get('link')
                    
            return details
            
        except Exception as e:
            # FIXED: This will print the exact reason it failed to your terminal!
            print(f"Details attempt {attempt + 1} failed for movie {movie_id}. Error: {e}")
            time.sleep(1)
            
    # If it fails all 3 tries, return None
    return None

def recommend(movie):
    """Finds the 5 similar movies and returns their IDs so we can click on them."""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recs = []
    for i in movies_list:
        m_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster = fetch_poster_only(m_id)
        recs.append({'id': m_id, 'title': title, 'poster': poster})
        time.sleep(0.2)
    return recs


# --- CALLBACK FUNCTIONS ---

def go_to_details(movie_id):
    st.session_state.selected_movie_id = movie_id
    st.session_state.current_page = "details"

def go_to_home():
    st.session_state.current_page = "home"


# --- LOAD DATA ---
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# --- WEB PAGE UI ROUTING ---

if st.session_state.current_page == "home":
    st.title("🍿 Cinematic Recommendation Engine")
    
    selected_movie = st.selectbox("Search for a movie:", movies['title'].values)
    
    if st.button("Recommend", type="primary"):
        with st.spinner('Consulting the TMDB database...'):
            st.session_state.recommendations = recommend(selected_movie)
            
    if st.session_state.recommendations:
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        
        for i in range(5):
            with cols[i]:
                st.image(st.session_state.recommendations[i]['poster'], width=150)
                st.write(f"**{st.session_state.recommendations[i]['title']}**")
                
                st.button(
                    "View Details", 
                    key=f"btn_{st.session_state.recommendations[i]['id']}", 
                    on_click=go_to_details, 
                    args=(st.session_state.recommendations[i]['id'],)
                )

elif st.session_state.current_page == "details":
    
    st.button("⬅️ Back to Recommendations", on_click=go_to_home)
        
    with st.spinner("Fetching full movie dossier..."):
        details = fetch_full_details(st.session_state.selected_movie_id)
        
    if details:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(details['poster'], use_container_width=True)
            if details['watch_link']:
                st.markdown(f"### [🍿 Click Here to see Where to Watch]({details['watch_link']})")
            
        with col2:
            st.title(details['title'])
            st.write(f"**Release Date:** {details['release_date']}")
            st.write(f"**TMDB Rating:** ⭐ {details['rating']} / 10")
            
            formatted_revenue = f"${details['revenue']:,}" if details['revenue'] > 0 else "Unknown"
            st.write(f"**Box Office:** {formatted_revenue}")
            
            st.subheader("Plot Summary")
            st.write(details['overview'])
            
        st.divider()
        
        st.subheader("Top Cast")
        if details['cast']:
            cast_cols = st.columns(5)
            for i, actor in enumerate(details['cast']):
                with cast_cols[i]:
                    st.image(actor['pic'], width=120)
                    st.write(f"**{actor['name']}**")
                    st.caption(f"as {actor['character']}")
        else:
            st.write("Cast data not available.")
            
        st.divider()
        
        st.subheader("Top Reviews")
        if details['reviews']:
            for review in details['reviews']:
                with st.chat_message("user"):
                    st.write(f"**{review['author']}** said:")
                    st.write(review['content'])
        else:
            st.write("No featured reviews found.")
            
    else:
        st.error("Failed to load details. TMDB might be missing data for this specific movie.")