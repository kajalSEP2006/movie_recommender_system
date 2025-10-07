import streamlit as st
import pandas as pd
import pickle
import requests
import time

def fetch_poster(movie_id):
       response = requests.get(
           f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c26088eb9e62e4b656f30a7b1e085cad&language=en-US'
       )
       data = response.json()
       poster_path = data.get('poster_path')  # safer
       if poster_path:
           return "https://image.tmdb.org/t/p/w185" + poster_path
       else:
           return "https://via.placeholder.com/185x278?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarty[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].title

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].id))

        time.sleep(0.2)  # 200ms delay between requests

    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarty = pickle.load(open('similarty.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    import streamlit as st

    col1, col2, col3,col4,col5 = st.columns(5)

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




































