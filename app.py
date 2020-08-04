
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db

import os


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

APP = create_app()


# ROUTES
@APP.route('/')
def default_route():
  print("Default route")
  return jsonify({
    "success": True
  })


@APP.route('/actors', methods=["POST"])
def new_actor():
  print("NEW actor")
  return jsonify({
    "success": True
  })


@APP.route('/actors-detail', methods=["GET"])
def list_actors():
  print("Actors list")
  return jsonify({
    "success": True
  })


@APP.route('/actors/<int:actor_id>', methods=["PATCH"])
def update_actor(actor_id):
  print("UPDATE actor")
  return jsonify({
    "success": True
  })


@APP.route('/actors/<int:actor_id>', methods=["DELETE"])
def delete_actor(actor_id):
  print("DELETE actor")
  return jsonify({
    "success": True
  })


@APP.route('/movies', methods=["POST"])
def new_movie():
  print("NEW movie")
  return jsonify({
    "success": True
  })


@APP.route('/movies-detail', methods=["GET"])
def list_movies():
  print("Movies list")
  return jsonify({
    "success": True
  })


@APP.route('/movies/<int:movie_id>', methods=["PATCH"])
def update_movie(movie_id):
  print("UPDATE movie")
  return jsonify({
    "success": True
  })


@APP.route('/movies/<int:movie_id>', methods=["DELETE"])
def delete_movie(movie_id):
  print("DELETE movie")
  return jsonify({
    "success": True
  })



if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
