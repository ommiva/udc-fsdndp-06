
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Actor, Movie, Cast

import os
import sys
import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ROUTES
    @app.route('/', methods=["GET"])
    def default_route():
        print("Default route")
        return jsonify({
            "success": True
        })

    @app.route('/actors', methods=["POST"])
    def new_actor():
        print("NEW actor")

        body = request.get_json()
        try:
            new_name = body.get('name', None)
            new_age = body.get('age', 0)
            new_gender = body.get('gender', None)

            if new_name is None:
                abort(400)

            actor = Actor(
                name=new_name,
                age=new_age,
                gender=new_gender
            )

            actor.insert()

            return jsonify({
                "success": True,
                "actor": actor.format()
            }), 201

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors-detail', methods=["GET"])
    def list_actors():
        print("Actors list")

        try:
            actors = Actor.query\
                .order_by(Actor.name)\
                .all()

            current_actors = [actor.format() for actor in actors]

            return jsonify({
                "actors": current_actors
            })
        except Exception as e:
            print(sys.exc_info)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    def update_actor(actor_id):
        print("UPDATE actor")
        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            else:

                if 'name' in body:
                    actor.name = body.get('name')

                if 'age' in body:
                    actor.age = body.get('age')

                if 'gender' in body:
                    actor.gender = body.get('gender')

                actor.update()

                return jsonify({
                    "success": True,
                    "actor": actor.format()
                })

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    def delete_actor(actor_id):
        print("DELETE actor")

        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()

            if actor is None:
                abort(404)
            else:
                actor.delete()

                return jsonify({
                    "success": True,
                    "delete": actor_id
                })

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies', methods=["POST"])
    def new_movie():
        print("NEW movie")

        body = request.get_json()
        print("POST /movies | ", body)
        try:
            new_title = body.get('title', None)
            new_release = body.get('release_date', None)

            if new_title is None:
                abort(400)

            if new_release is not None:
                new_release = datetime.datetime.strptime(
                    new_release,
                    '%m/%d/%Y'
                )

            movie = Movie(
                title=new_title,
                release_date=new_release
            )

            movie.insert()

            return jsonify({
                "success": True,
                "movie": movie.format()
            }), 201

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies-detail', methods=["GET"])
    def list_movies():
        print("Movies list")
        try:
            movies = Movie.query\
                .order_by(Movie.title)\
                .all()

            current_movies = [movie.format() for movie in movies]

            return jsonify({
                "movies": current_movies
            })
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    def update_movie(movie_id):
        print("UPDATE movie")
        body = request.get_json()

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            else:
                if 'title' in body:
                    movie.title = body.get('title')

                if 'release_date' in body:

                    movie.release_date = format_datetime(
                        body.get('release_date'))

            movie.update()

            return jsonify({
                "success": True,
                "movie": movie.format()
            })

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    def delete_movie(movie_id):
        print("DELETE movie")

        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()

            if movie is None:
                abort(404)
            else:
                movie.delete()

                return jsonify({
                    "success": True,
                    "delete": movie_id
                })

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "Unprocessable"
                }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "Resource not found"
                }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "Bad Request"
                }), 400

    return app


# Auxiliars


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = " MM/dd/yyyy h:mma"
    elif format == 'medium':
        format = "MM/dd/yyyy"
    return babel.dates.format_datetime(date, format)

# ------------------------------------------------


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
