import streamlit as st
import pickle
import pandas as pd
import requests
import os

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API')

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key))
    data = response.json()
    # print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:26]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch movie poster from tmdb API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    num_columns = 5
    num_elements_per_column = len(names) // num_columns

    col1, col2, col3, col4, col5 = st.columns(num_columns)

    for i in range(num_elements_per_column):
        with col1:
            st.text(names[i])
            st.image(posters[i])

        with col2:
            st.text(names[i + num_elements_per_column])
            st.image(posters[i + num_elements_per_column])

        with col3:
            st.text(names[i + 2 * num_elements_per_column])
            st.image(posters[i + 2 * num_elements_per_column])

        with col4:
            st.text(names[i + 3 * num_elements_per_column])
            st.image(posters[i + 3 * num_elements_per_column])

        with col5:
            st.text(names[i + 4 * num_elements_per_column])
            st.image(posters[i + 4 * num_elements_per_column])

