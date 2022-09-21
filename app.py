# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from config import db, app
from models import Movie, Director, Genre
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
        """Возвращает список всех фильмов"""
        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200

    def post(self):
        """Добовляем фильм"""
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id: int):
        """Возвращает фильм по id"""
        try:
            one_movie = Movie.query.filter(Movie.id == id).one()
            return movie_schema.dump(one_movie), 200
        except Exception as error:
            return str(error), 404

    def put(self, id: int):
        """Обновляет фильм"""
        try:
            movie = Movie.query.filter(Movie.id == id).one()
            req_json = request.json

            movie.title = req_json.get("title")
            movie.description = req_json.get("description")
            movie.trailer = req_json.get("trailer")
            movie.year = req_json.get("year")
            movie.rating = req_json.get("rating")
            movie.genre_id = req_json.get("genre_id")
            movie.director_id = req_json.get("director_id")

            db.session.add(movie)
            db.session.commit()
        except Exception as error:
            return str(error), 404

    def delete(self, id: int):
        """Удаляем фильм"""
        movie = Movie.query.filter(Movie.id == id).one()
        db.session.delete(movie)
        db.session.commit()
        return "", 404




@movie_ns.route("/directors/<int:uid>")
class DirectorsViews(Resource):
    def get(self, uid: int):
        """Получаем все фильмы режиссера по его id """
        try:
            movies_by_director = Movie.query.filter(Movie.director_id == uid).all()
            return movies_schema.dump(movies_by_director), 200
        except Exception:
            return "", 404
    def put(self, id: int):
        """Обновляет режжисера"""
        try:
            director = Director.query.filter(Director.id == id).one()
            req_json = request.json

            director.name = req_json.get("name")

            db.session.add(director)
            db.session.commit()
        except Exception as error:
            return str(error), 404

    def delete(self, id: int):
        """Удаляем режжисера"""
        director = Director.query.filter(Director.id == id).one()
        db.session.delete(director)
        db.session.commit()
        return "", 404


@movie_ns.route("/genres/<int:uid>")
class GenresViews(Resource):
    def get(self, uid: int):
        """Получаем все фильмы одного жанра по его id """
        try:
            movies_by_genres = Movie.query.filter(Movie.genre_id == uid).all()
            return movies_schema.dump(movies_by_genres), 200
        except Exception:
            return "", 404
    def put(self, id: int):
        """Обновляет жанр"""
        try:
            genre = Genre.query.filter(Genre.id == id).one()
            req_json = request.json

            genre.name = req_json.get("name")

            db.session.add(genre)
            db.session.commit()
        except Exception as error:
            return str(error), 404

    def delete(self, id: int):
        """Удаляем жанр"""
        genre = Genre.query.filter(Genre.id == id).one()
        db.session.delete(genre)
        db.session.commit()
        return "", 404


if __name__ == '__main__':
    app.run(debug=True)
