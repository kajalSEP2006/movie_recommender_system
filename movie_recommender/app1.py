import requests


def fetch_poster(movie_id):
    """
    Fetches the poster URL for a given movie ID from TMDB.
    Returns a placeholder image if the request fails.
    """
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c26088eb9e62e4b656f30a7b1e085cad&language=en-US',
            timeout=5  # waits max 5 seconds
        )
        response.raise_for_status()  # raises error for bad responses
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(selected_movie_name, movies, similarity):
    """
    Returns recommended movie names and their posters.
    movies: DataFrame with movie info
    similarity: precomputed similarity matrix
    """
    try:
        # Find index of selected movie
        idx = movies[movies['title'] == selected_movie_name].index[0]
        # Get similarity scores for all movies
        sim_scores = list(enumerate(similarity[idx]))
        # Sort movies based on similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Get top 5 recommendations (skip the first one as it's the same movie)
        sim_scores = sim_scores[1:6]

        recommended_movies_names = []
        recommended_movies_posters = []

        for i in sim_scores:
            movie_id = movies.iloc[i[0]].id
            recommended_movies_names.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))

        return recommended_movies_names, recommended_movies_posters

    except Exception as e:
        print("Error in recommendation:", e)
        return [], []
