# Movie Recommendation System

This project implements a movie recommendation system based on collaborative filtering using the MovieLens 100k dataset. It provides two interfaces: a RESTful API built with Flask and an interactive web application built with Streamlit.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Dataset](#dataset)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Local Setup (Flask)](#local-setup-flask)
  - [Local Setup (Streamlit)](#local-setup-streamlit)
  - [Deployment to Streamlit Cloud](#deployment-to-streamlit-cloud)
- [Usage](#usage)
  - [Flask API Usage](#flask-api-usage)
  - [Streamlit App Usage](#streamlit-app-usage)

## Project Overview

This system recommends movies to users by finding other movies that are highly correlated with a selected movie based on user rating patterns. The core logic involves creating a user-item matrix from historical ratings and calculating Pearson correlation coefficients between movies. Recommendations are filtered to include only movies with a sufficient number of ratings to ensure reliability.

## Features

- **Collaborative Filtering:** Recommends movies based on similarity in user ratings.
- **Flask API:** Provides a programmatic interface to get movie recommendations.
- **Streamlit Web Application:** Offers an interactive and user-friendly interface for selecting a movie and viewing recommendations.
- **MovieLens 100k Dataset:** Utilizes a well-known dataset for movie ratings.

## Dataset

The project uses the [MovieLens 100k dataset](https://grouplens.org/datasets/movielens/100k/). This dataset contains 100,000 ratings from 943 users on 1,682 movies.

## Technologies Used

- Python 3.x
- Pandas: For data manipulation and analysis.
- Flask: For building the RESTful API.
- Streamlit: For creating the interactive web application.
- requests: For downloading the dataset.
- zipfile, io, os: For file operations.
- pyngrok: For exposing local servers to the internet (used in development, not typically for production Streamlit Cloud).

## Getting Started

To get a copy of the project up and running on your local machine, follow these steps.

### Prerequisites

Ensure you have Python 3.x installed. You can install the necessary libraries using pip:

```bash
pip install pandas flask streamlit requests pyngrok
```

### Local Setup (Flask)

1.  **Clone the repository (or copy `app.py`):**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Run the Flask application:**

    The `app.py` file contains the Flask server. When run, it will download the MovieLens 100k dataset if it's not already present.

    ```bash
    python app.py
    ```

    The Flask app will typically run on `http://127.0.0.1:5001/`.

3.  **Expose the Flask app (optional, using ngrok for testing):**

    If you want to access your Flask app from outside your local machine (e.g., from Colab), you can use `ngrok`.
    
    *   First, get an ngrok auth token from [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken).
    *   Then, you would run a script similar to the one below (this was used in the Colab notebook):

    ```python
    from pyngrok import ngrok, conf
    import os
    import subprocess
    import time

    NGROK_AUTH_TOKEN = "YOUR_NGROK_AUTH_TOKEN" # Replace with your token

    try:
        ngrok.kill()
        conf.get_default().auth_token = NGROK_AUTH_TOKEN
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)

        flask_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)

        public_url = ngrok.connect(5001).public_url # Connect to the Flask port
        print(f"* ngrok tunnel URL: {public_url}")
        print(f"* Flask app running on: http://127.0.0.1:5001/")
        print(f"* Access your recommendations API at: {public_url}/recommend?movie=Toy%20Story%20(1995)")

    except Exception as e:
        print(f"Error starting ngrok or Flask app: {e}")
    ```

### Local Setup (Streamlit)

1.  **Clone the repository (or copy `streamlit_app.py` and `requirements.txt`):**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Run the Streamlit application:**

    The `streamlit_app.py` file contains the Streamlit application. When run, it will download the MovieLens 100k dataset if it's not already present.

    ```bash
    streamlit run streamlit_app.py
    ```

    This will open the Streamlit app in your web browser, usually at `http://localhost:8501/`.

### Deployment to Streamlit Cloud

1.  **Prepare your GitHub Repository:**
    *   Ensure your GitHub repository contains `streamlit_app.py` and `requirements.txt` in the root directory.
    *   **Crucially, do NOT include `app.py` (the Flask app) in the repository you intend to deploy to Streamlit Cloud.** This can cause conflicts or lead to incorrect deployment attempts.
    *   The `ml-100k` dataset should *not* be committed to Git; `streamlit_app.py` handles its download.

2.  **Deploy via Streamlit Cloud:**
    *   Go to [Streamlit Cloud](https://share.streamlit.io/) and log in with your GitHub account.
    *   Click "New app" and select your prepared GitHub repository.
    *   Set "Main file path" to `streamlit_app.py`.
    *   Click "Deploy!"

## Usage

### Flask API Usage

Once the Flask API is running (locally or via ngrok), you can make GET requests to the `/recommend` endpoint with a `movie` query parameter.

**Example Request (using `curl`):**

```bash
curl "http://127.0.0.1:5001/recommend?movie=Toy%20Story%20(1995)"
```

**Example Response:**

```json
{
  "Aladdin (1992)": {
    "Correlation": 0.6974108873,
    "RatingCount": 167
  },
  "Beauty and the Beast (1991)": {
    "Correlation": 0.6517596825,
    "RatingCount": 112
  },
  "Lion King, The (1994)": {
    "Correlation": 0.6508821935,
    "RatingCount": 152
  },
  "Independence Day (ID4) (1996)": {
    "Correlation": 0.5898869715,
    "RatingCount": 158
  },
  "Twelve Monkeys (1995)": {
    "Correlation": 0.5794827013,
    "RatingCount": 108
  },
  "Apollo 13 (1995)": {
    "Correlation": 0.5786737525,
    "RatingCount": 173
  },
  "Star Wars (1977)": {
    "Correlation": 0.5694212988,
    "RatingCount": 205
  },
  "Return of the Jedi (1983)": {
    "Correlation": 0.5592873499,
    "RatingCount": 142
  },
  "Raiders of the Lost Ark (1981)": {
    "Correlation": 0.5520935574,
    "RatingCount": 152
  },
  "Forrest Gump (1994)": {
    "Correlation": 0.5487679361,
    "RatingCount": 218
  }
}
```

### Streamlit App Usage

Open the Streamlit app in your browser (either locally or deployed to Streamlit Cloud). You will see a dropdown menu to select a movie. Choose a movie from the list and click the "Get Recommendations" button to view the top correlated movies.
