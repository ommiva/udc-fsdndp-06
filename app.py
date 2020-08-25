
from flask import Flask, request, abort, render_template, redirect
from flask import flash, jsonify
from flask_cors import CORS

from models import setup_db, Actor, Movie, Cast
from auth.auth import AuthError, requires_auth, AUTH0_DOMAIN
from datetime import datetime
from babel import Locale
from babel.dates import format_datetime
from werkzeug import exceptions

from authlib.integrations.flask_client import OAuth

import os
import sys
import dateutil.parser
import babel


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # TODO: Move to env

    domain = "omv-fsnd-casting.us.auth0.com"
    audience = "castingagency"
    client_id = "v13pFbBPOlvhNdvmss6QLe13L2gpz9To"
    redirect_url = "http://localhost:8080/login-results"

    # ROUTES
    @app.route('/', methods=["GET"])
    def index():
        return render_template('pages/home.html')

    @app.route('/login', methods=["GET"])
    def login():
        link =\
            f"https://{domain}/"\
            + f"authorize?audience={audience}"\
            + "&response_type=token"\
            + f"&client_id={client_id}"\
            + f"&redirect_uri={redirect_url}"
        print(link)
        return redirect(link)

    @app.route('/login-results', methods=["GET"])
    def login_config():
        # TODO:
        print(request.url)
        return render_template('pages/dummy.html')

    @app.route('/intro')
    def intro():
        return render_template('pages/index.html')

    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def new_actor():
        print("NEW actor")

        body = request.get_data()
        print("POST /actors | ", body)
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

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors-detail', methods=["GET"])
    @requires_auth('get:actors-detail')
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
    @requires_auth('patch:actors')
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

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth('delete:actors')
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

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
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
                new_release = datetime.strptime(
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

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print("Error > ", e)
            print(sys.exc_info())
            abort(422)

    @app.route('/movies-detail', methods=["GET"])
    @requires_auth('get:movies-detail')
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
    @requires_auth('patch:movies')
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

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth('delete:movies')
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

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        print(" <<<< Error 422 - ", error)
        return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "Unprocessable"
                }), 422

    @app.errorhandler(404)
    def not_found(error):
        print(" <<<< Error 404 - ", error)
        return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "Resource not found"
                }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        print(" <<<< Error 405 - ", error)
        return jsonify({
                    "success": False,
                    "error": 405,
                    "message": "Method not allowed"
                }), 405

    @app.errorhandler(400)
    def bad_request(error):
        print(" <<<< Error 400 - ", error)
        return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "Bad Request"
                }), 400

    @app.errorhandler(AuthError)
    def authentication_error(error):
        """
        Implements error handler for AuthError
        """
        print(" <<<< Error AuthError - ", error)
        return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error["description"]
                }), error.status_code

    return app


# Auxiliars


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = " MM/dd/yyyy h:mma"
    elif format == 'medium':
        format = "MM/dd/yyyy"
    return babel.dates.format_datetime(
        date,
        format=format,
        locale=Locale('en', 'US'))

# ------------------------------------------------


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
