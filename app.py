
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Actor, Movie, Cast

import os
import sys


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
        return jsonify({
            "success": True
        })

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
        return jsonify({
            "success": True
        })

    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    def delete_actor(actor_id):
        print("DELETE actor")
        return jsonify({
            "success": True
        })

    @app.route('/movies', methods=["POST"])
    def new_movie():
        print("NEW movie")
        return jsonify({
            "success": True
        })

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
        return jsonify({
            "success": True
        })

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    def delete_movie(movie_id):
        print("DELETE movie")
        return jsonify({
            "success": True
        })

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
                })

    return app

# ------------------------------------------------


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
