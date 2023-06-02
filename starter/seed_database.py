import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

def load_movies():
    """Load movies from JSON file into database."""

    with open("data/movies.json") as f:
        movie_data = json.loads(f.read())

    movies_in_db = []
    for movie in movie_data:
        title, overview, poster_path = (
            movie["title"],
            movie["overview"],
            movie["poster_path"],
        )
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

        db_movie = crud.create_movie(title, overview, release_date, poster_path)
        movies_in_db.append(db_movie)
    
    return movies_in_db


def create_users(num_users, num_ratings):
    """Create fake users and ratings for testing and development."""

    for n in range(num_users):
        email = f"user{n}@test.com"
        password = "test"

        user = crud.create_user(email, password)

        for _ in range(num_ratings):
            random_movie = choice(movies_in_db)
            score = randint(1, 5)

            rating = crud.create_rating(user, random_movie, score)


if __name__ == "__main__":
    with server.app.app_context():
        model.connect_to_db(server.app)
        model.db.create_all()

        movies_in_db = load_movies()
        create_users(10, 10)

        model.db.session.commit()