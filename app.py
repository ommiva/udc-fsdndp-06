
from flask import Flask, request, abort, render_template, redirect
from flask import flash, jsonify
from flask_cors import CORS

from models import setup_db, Actor, Movie, Cast
from models import bulk_delete_cast_by_movie
from auth.auth import AuthError, requires_auth
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
    # Front-end
    @app.route('/', methods=["GET"])
    @app.route('/default')
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
        return render_template('pages/authbridge.html')

    @app.route('/intro')
    def intro():
        return render_template('pages/index.html')

    @app.route('/actors-list')
    def actors():
        return render_template('pages/show_actors.html')

    @app.route('/movies-list')
    def movies():
        return render_template('pages/show_movies.html')
    
    @app.route('/logout')
    def logout():
        link = f'https://{domain}/v2/'\
            + 'logout?returnTo=http%3A%2F%2Flocalhost:8080'\
            + f'&client_id={client_id}'
        return redirect(link)

    # API
    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def new_actor():
        print("NEW actor")

        body = request.get_json()
        print("POST /actors | ", body)
        try:
            new_name = body.get('name', None)
            new_age = body.get('age', 0)
            new_gender = body.get('gender', None)

            if new_name is None or not new_name:
                abort(400)
                
            if not new_age:
                new_age = 0
            
            if new_gender == 'Select':
                new_gender = ''

            actor = Actor(
                name=new_name.strip(),
                age=new_age,
                gender=new_gender.strip()
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

            if new_title is None or not new_title:
                abort(400)

            if new_release is not None and new_release:
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

    @app.route('/cast-detail', methods=["GET"])
    @requires_auth('get:cast-detail')
    def list_cast():
        print("Cast list")
        try:
            data = []
            cast_list = Cast.query.all()

            current_cast = [cast.format() for cast in cast_list]

            # print("Casting ", current_cast)
            # print("list: ", len(data))
            if not len(current_cast):
                abort(404)

            return jsonify({
                "cast": current_cast
            })

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/cast', methods=["POST"])
    @requires_auth('post:casting')
    def new_cast():
        print("New cast")

        body = request.get_json()

        try:
            actor_id = body.get("actor", None)
            movie_id = body.get("movie", None)

            if actor_id is None \
               or movie_id is None \
               or not actor_id \
               or not movie_id:
                abort(400)

            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            movie = Movie.query.filter_by(id=movie_id).one_or_none()

            if actor is None or movie is None:
                abort(404)

            casting = Cast(
                actor_id=actor.id,
                movie_id=movie.id
                )
            casting.insert()

            return jsonify({
                "success": True,
                "cast": casting.format()
            }), 201

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/cast/<int:cast_id>', methods=["DELETE"])
    @requires_auth("delete:casting-actor")
    def delete_casting_actor(cast_id):
        try:
            cast = Cast.query.filter_by(id=cast_id).one_or_none()

            if cast is None:
                abort(404)

            deleted = cast.format()
            cast.delete()

            return jsonify({
                "success": True,
                "delete": deleted
            })

        except exceptions.HTTPException as httpe:
            print("Error HTTP > ", httpe)
            raise
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/cast-movie/<int:movie_id>', methods=["DELETE"])
    @requires_auth("delete:casting-movie")
    def delete_casting_movie(movie_id):
        try:
            casting_movie_total = Cast.query\
                .filter_by(movie_id=movie_id).count()

            if casting_movie_total == 0:
                abort(404)

            bulk_delete_cast_by_movie(movie_id)

            return jsonify({
                "success": True,
                "delete": casting_movie_total
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
