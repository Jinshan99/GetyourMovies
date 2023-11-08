import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import bz2
import _pickle as cPickle
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=dd311ecc0ab3b8fea1c4e100792ed2c0&&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie, movies_data):
    movie_index = movies_data[movies_data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list_ = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list_:
        movie_id = movies_data.iloc[i[0]].movie_id
        recommended_movies.append(movies_data.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters
def decompress_pickle(file):
    # data = bz2.BZ2File(file, 'rb')
    with bz2.BZ2File(file, 'rb') as f:
        data = cPickle.load(f)
    # data = cPickle.load(data)
    return data
movies_list = decompress_pickle('movies.pbz2')
similarity = decompress_pickle('similarity.pbz2')
# movies_list = pd.read_pickle('movies.pkl')
# similarity = pd.read_pickle('similarity.pkl')
# movies_list = pickle.load(open('movies.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_data = pd.DataFrame(movies_list)  # Assuming movies_list contains a list of dictionaries or a suitable structure

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie:', movies_data['title'].values)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, movies_data)
    col1, col2, col3, col4, col5 = st.beta_columns(5) #, col4, col5
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
