from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from app import create_app
from models import setup_db, Actor, Movie, Cast

import os
import unittest
import json


class MoviesTestCase(unittest.TestCase):
    """ Represents the casting test case """

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}"\
            .format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

            setUp_deleted()

        self.new_actor = {
            "name": "Goldie Hawn",
            "age": 74,
            "gender": "Female"
        }

        self.new_movie = {
            "title": "The game",
            "release_date": "09/12/1997"
        }

    def tearDown(self):
        """ Execute after reach test """
        pass

    # Test definitions
    # Dummy >>>>>>>>>>>>>>>>>>>>>>>>>>
    def test_default(self):
        res = self.client().get("/")
        # data = res.get_json(res.data)

        self.assertEqual(res.status_code, 200)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def test_get_all_actors(self):
        res = self.client().get("/actors-detail")
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actors"])
    
    # TODO: test for fail get /actors-detail

    def test_get_all_movies(self):
        res = self.client().get("/movies-detail")
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movies"])
    
    # TODO: test for fail get /movies-detail

    def test_add_new_actor(self):
        res = self.client().post("/actors", json=self.new_actor)

        self.assertEqual(res.status_code, 200)
    
    def test_add_new_movie(self):
        res = self.client().post("/movies", json=self.new_movie)

        self.assertEqual(res.status_code, 200)
    
    def test_update_actor(self):
        res = self.client().patch("/actors/2", json={"name": "Kurt Russell"})

        self.assertEqual(res.status_code, 200)
    
    def test_update_movie(self):
        res = self.client().patch("/movies/2", json={"title": "Jaws 3"})

        self.assertEqual(res.status_code, 200)

    def test_delete_actor(self):
        res = self.client().delete("/actors/1")

        self.assertEqual(res.status_code, 200)
    
    def test_delete_movie(self):
        res = self.client().delete("/movies/1")

        self.assertEqual(res.status_code, 200)

def setUp_deleted():
    """ Updates database ton include deleted data """
    print("Restore deleted rows")

    deleted_actor = Actor.query\
        .filter(Actor.id == 1)\
        .one_or_none()
    if deleted_actor is None:
        actor = Actor(name="Harrison Ford",
                      age=78,
                      gender="Male")
        actor.id = 1
        actor.insert()

    deleted_movie = Movie.query\
        .filter(Movie.id == 1)\
        .one_or_none()
    if deleted_movie is None:
        movie = Movie(title="The Dark Knight ",
                      release_date="07/14/2008")
        movie.id = 1
        movie.insert()


# Mtext executable
if __name__ == "__main__":
    unittest.main()
