import pickle
import streamlit as st
import requests

# ✅ Fetch poster, IMDb link, and rating
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    
    poster_path = data.get('poster_path', '')
    imdb_id = data.get('imdb_id', '')
    rating = data.get('vote_average', 'N/A')
    
    full_poster_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    imdb_link = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else ""
    
    return full_poster_path, imdb_link, rating

# ✅ Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    names, posters, links, ratings = [], [], [], []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, imdb_link, rating = fetch_movie_details(movie_id)
        names.append(movies.iloc[i[0]].title)
        posters.append(poster)
        links.append(imdb_link)
        ratings.append(rating)

    return names, posters, links, ratings

# ✅ Streamlit UI
st.set_page_config(layout="wide")
st.header('🎥 Movie Recommender System')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# ✅ Styling for the movie cards
st.markdown("""
    <style>
    .movie-card {
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        height: 100%;
    }
    .movie-card:hover {
        transform: scale(1.05);
        background-color: #ffffff;
    }
    .movie-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 5px;
        color: #0066cc;
        text-decoration: none;
    }
    .movie-rating {
        font-size: 16px;
        color: #ff9900;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Display Recommendations
if st.button('Show Recommendation'):
    names, posters, links, ratings = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
                <div class="movie-card">
                    <a href="{links[i]}" target="_blank" class="movie-title">{names[i]}</a>
                    <div class="movie-rating">⭐ {ratings[i]}/10</div>
                    <img src="{posters[i]}" width="100%" style="border-radius: 10px;" />
                </div>
            """, unsafe_allow_html=True)

