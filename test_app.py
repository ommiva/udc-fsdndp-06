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

            self.setUp_deleted

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

    def test_default(self):
        res = self.client().get("/")
        # data = res.get_json(res.data)

        self.assertEqual(res.status_code, 200)


# Mtext executable
if __name__ == "__main__":
    unittest.main()
