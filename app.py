
from flask import Flask, request, jsonify
import pandas as pd
import os
import zipfile
import io
import requests

app = Flask(__name__)

# --- Data Loading and Preprocessing (Copied from previous steps) ---
# Define the URL for the MovieLens 100k dataset
MOVIES_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'
DATA_DIR = './ml-100k'

# Download and extract the dataset if not already present
if not os.path.exists(DATA_DIR):
    print("Downloading MovieLens 100k dataset...")
    response = requests.get(MOVIES_URL)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall('.')
    print("Download and extraction complete.")

# Define column names based on the dataset's README
ratings_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings_df = pd.read_csv(os.path.join(DATA_DIR, 'u.data'), sep='\t', names=ratings_cols, encoding='latin-1')

movie_cols = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL',
              'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy',
              'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
              'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies_df = pd.read_csv(os.path.join(DATA_DIR, 'u.item'), sep='|', names=movie_cols, encoding='latin-1')

# Drop unnecessary columns and merge
movies_df_cleaned = movies_df.drop(columns=['release_date', 'video_release_date', 'IMDb_URL'])
ratings_df = ratings_df.drop(columns=['timestamp'])
merged_df = pd.merge(ratings_df, movies_df_cleaned, on='movie_id')

# Create user-item matrix
user_movie_matrix = merged_df.pivot_table(index='user_id', columns='movie_title', values='rating')

# --- Recommendation Function (Copied from previous steps) ---
def recommend_movies(movie_title, user_movie_matrix, num_recommendations=10):
    try:
        movie_ratings = user_movie_matrix[movie_title]
    except KeyError:
        return pd.Series(dtype=float) # Return empty series for consistency

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

# --- Flask Routes ---
@app.route('/recommend', methods=['GET'])
def get_recommendations():
    movie_title = request.args.get('movie')
    if not movie_title:
        return jsonify({'error': 'Please provide a movie title as a query parameter (e.g., /recommend?movie=Toy Story (1995))'}), 400

    recommendations = recommend_movies(movie_title, user_movie_matrix)

    if recommendations.empty:
        return jsonify({'message': f"No recommendations found for '{movie_title}'. It might not be in the dataset or have enough ratings."}), 404
    else:
        return jsonify(recommendations.to_dict(orient='index'))

@app.route('/')
def home():
    return "<h1>Movie Recommendation API</h1><p>Use /recommend?movie=<movie_title> to get recommendations.</p>"

if __name__ == '__main__':
    # Running on port 5003 now instead of 5002
    app.run(host='127.0.0.1', port=5003)
