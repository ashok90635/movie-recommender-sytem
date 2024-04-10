import streamlit as st
import pickle
import requests

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list = movies['title'].values

st.header("Movie Recommender System")
select_value = st.selectbox("Select movies from dropdown", movies_list)

def fetch_poster(movie_id):
    api_key = "420e5a7ff8d4447c92296f7f6281f1d5"  # Add your API key here
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url)
    data = data.json()
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]]['id']
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommend_movie.append(movies.iloc[i[0]]['title'])
            recommend_poster.append(poster_url)
    return recommend_movie, recommend_poster

if st.button("Show Recommendations"):
    movie_names, movies_poster = recommend(select_value)
    if movie_names:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(movie_names[0])
            st.image(movies_poster[0])
        with col2:
            st.text(movie_names[1])
            st.image(movies_poster[1])
        with col3:
            st.text(movie_names[2])
            st.image(movies_poster[2])
        with col4:
            st.text(movie_names[3])
            st.image(movies_poster[3])
        with col5:
            st.text(movie_names[4])
            st.image(movies_poster[4])
    else:
        st.write("No recommendations found for this movie.")
