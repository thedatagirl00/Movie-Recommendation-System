

import streamlit as st
import pandas as pd
import os
import zipfile
import io
import requests

st.title('Movie Recommendation System')

# --- Data Loading and Preprocessing ---
@st.cache_data # Cache data loading to avoid re-running on every interaction
def load_data():
    MOVIES_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'
    DATA_DIR = './ml-100k'

    if not os.path.exists(DATA_DIR):
        # st.write("Downloading MovieLens 100k dataset...") # Removed st.write statement
        response = requests.get(MOVIES_URL)
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall('.')
        # st.write("Download and extraction complete.") # Removed st.write statement

    ratings_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings_df = pd.read_csv(os.path.join(DATA_DIR, 'u.data'), sep='\t', names=ratings_cols, encoding='latin-1')

    movie_cols = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL',
                  'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy',
                  'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                  'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    movies_df = pd.read_csv(os.path.join(DATA_DIR, 'u.item'), sep='|', names=movie_cols, encoding='latin-1')

    movies_df_cleaned = movies_df.drop(columns=['release_date', 'video_release_date', 'IMDb_URL'])
    ratings_df = ratings_df.drop(columns=['timestamp'])
    merged_df = pd.merge(ratings_df, movies_df_cleaned, on='movie_id')

    user_movie_matrix = merged_df.pivot_table(index='user_id', columns='movie_title', values='rating')
    return user_movie_matrix, movies_df # Return movies_df to get all movie titles

user_movie_matrix, movies_df = load_data()

# --- Recommendation Function ---
@st.cache_data # Cache the recommendation function as well
def recommend_movies(movie_title, user_movie_matrix, num_recommendations=10):
    try:
        movie_ratings = user_movie_matrix[movie_title]
    except KeyError:
        return pd.Series(dtype=float)

    similar_to_movie = user_movie_matrix.corrwith(movie_ratings)
    corr_movie = pd.DataFrame(similar_to_movie, columns=['Correlation'])
    corr_movie.dropna(inplace=True)

    movie_ratings_count = user_movie_matrix.count()
    movie_ratings_count_df = pd.DataFrame(movie_ratings_count, columns=['RatingCount'])
    corr_movie = corr_movie.merge(movie_ratings_count_df, left_index=True, right_index=True)

    min_ratings_threshold = 100
    corr_movie = corr_movie[corr_movie['RatingCount'] >= min_ratings_threshold]

    recommendations = corr_movie.sort_values('Correlation', ascending=False)
    recommendations = recommendations[recommendations.index != movie_title]

    return recommendations.head(num_recommendations)

# --- Streamlit UI ---
st.header('Get Movie Recommendations')

# Get a list of all movie titles for the dropdown
all_movie_titles = sorted(movies_df['movie_title'].unique().tolist())

selected_movie = st.selectbox(
    'Choose a movie:',
    all_movie_titles
)

if st.button('Get Recommendations'):
    if selected_movie:
        st.write(f"## Recommendations for '{selected_movie}':")
        recommendations = recommend_movies(selected_movie, user_movie_matrix)

        if recommendations.empty:
            st.write(f"No recommendations found for '{selected_movie}'. It might not be in the dataset or have enough ratings.")
        else:
            # Display recommendations in a nice format
            st.table(recommendations.reset_index().rename(columns={'index': 'Movie Title', 'Correlation': 'Similarity Score'}))
    else:
        st.write("Please select a movie to get recommendations.")
