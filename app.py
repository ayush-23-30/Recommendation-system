# import streamlit as st
# import pickle 
# import requests

# # Load movie list and similarity matrix
# movie_list = pickle.load(open('movies.pkl', 'rb'))
# movie_list_title = movie_list['title'].values
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# # Function to fetch poster from TMDb
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#     data = requests.get(url).json()
#     poster_path = data.get('poster_path')
#     if poster_path:
#         return f"https://image.tmdb.org/t/p/w500/{poster_path}"
#     else:
#         return "https://via.placeholder.com/500x750?text=No+Image"

# # Recommendation function
# def recommeded(movie):
#     movie_index = movie_list[movie_list['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movie_names = []
#     recommended_movie_posters = []

#     for i in recommended_movies:
#         movie_id = movie_list.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movie_list.iloc[i[0]].title)

#     return recommended_movie_names, recommended_movie_posters

# # Streamlit UI
# st.title('Movie Recommendation System')
# select_movie_name = st.selectbox('Please Enter a Movie Name', movie_list_title)

# if st.button('Show Recommendation'):
#     with st.spinner('Fetching recommendations...'):
#         recommended_movie_names, recommended_movie_posters = recommeded(select_movie_name)
    
#     col1, col2, col3, col4, col5 = st.columns(5)
    
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])

import streamlit as st
import pickle
import requests
import gdown
import io

# import streamlit as st


# -------------------------
# Load movies.pkl (must be local)
# -------------------------
try:
    movie_list = pickle.load(open('movies.pkl', 'rb'))
    movie_list_title = movie_list['title'].values
except Exception as e:
    st.error(f"Failed to load movies.pkl: {e}")
    st.stop()

# -------------------------
# Cache and load similarity.pkl from Google Drive (in-memory)
# -------------------------
SIMILARITY_FILE_ID = "1nWamBufhl0G9l_AX736HOcOVa7Xex8x2"
SIMILARITY_URL = f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}"

@st.cache_resource(show_spinner="Please wait Data is Fetching may take 20-30 sec...")
def load_similarity():
    output = io.BytesIO()
    gdown.download(SIMILARITY_URL, output, quiet=True)
    output.seek(0)
    return pickle.load(output)

similarity = load_similarity()

# -------------------------
# Fetch poster helper
# -------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# -------------------------
# Recommendation function
# -------------------------
def recommeded(movie):
    try:
        movie_index = movie_list[movie_list['title'] == movie].index[0]
    except IndexError:
        st.error("Selected movie not found.")
        return [], []

    distances = similarity[movie_index]
    recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in recommended_movies:
        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie_list.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# -------------------------
# Streamlit UI
# -------------------------
st.title('🎬 Movie Recommendation System')

select_movie_name = st.selectbox('Enter or Select a Movie', movie_list_title)

if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommeded(select_movie_name)

    if recommended_movie_names:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])
    else:
        st.write("No recommendations found.")
