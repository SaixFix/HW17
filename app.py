# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from config import db, app
from models import Movie
from schemas import MovieSchema, DirectorSchema, GenreSchema

api = Api(app)

# обьекты сериализации/десерализации
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

# создаем неймспейсы
movie_ns = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genre')


@movie_ns.route("/")
class MoviesViews(Resource):
    def get(self):
        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200


@movie_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id: int):
        try:
            one_movie = Movie.query.filter(Movie.id == id).one()
            return movie_schema.dump(one_movie), 200
        except Exception:
            return "", 404


@movie_ns.route("/directors/<int:uid>")
class DirectorsViews(Resource):
    """Получаем все фильмы режиссера по его id """
    def get(self, uid: int):
        try:
            movies_by_director = Movie.query.filter(Movie.director_id == uid).all()
            return movies_schema.dump(movies_by_director), 200
        except Exception:
            return "", 404


@movie_ns.route("/genres/<int:uid>")
class GenresViews(Resource):
    """Получаем все фильмы одного жанра по его id """
    def get(self, uid: int):
        try:
            movies_by_genres = Movie.query.filter(Movie.genre_id == uid).all()
            return movies_schema.dump(movies_by_genres), 200
        except Exception:
            return "", 404


if __name__ == '__main__':
    app.run(debug=True)
