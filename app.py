import streamlit as st
import joblib
import pandas as pd
import requests

# Load data
movie_list = joblib.load('movies_df.joblib')
movie = pd.DataFrame(movie_list)

similarity = joblib.load('similarity_new.joblib')

# Custom Styling
st.markdown(
    """
    <style>
    .title-container {
        background-color: #FF5733;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background-color: #f4f4f4;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
        border-radius: 8px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title-container">🎬 Movie Recommender System</div>', unsafe_allow_html=True)

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b2b6bf763ec7191091d9b8803ad1866c&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/150"

# Recommendation function
def recommend(movies):
    movie_index = movie[movie['title'] == movies].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    movie_posters = []
    for i in movies_list:
        movie_id = movie.iloc[i[0]].id
        recommend_movies.append(movie.iloc[i[0]].title)
        movie_posters.append(fetch_poster(movie_id))
    
    return recommend_movies, movie_posters

# Sidebar for movie selection
selected_movie_name = st.sidebar.selectbox("🎥 Select a movie", movie['title'].values)

if st.sidebar.button("🔍 Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster, use_container_width=True)
