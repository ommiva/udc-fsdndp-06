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

        self.update_actor_data = "Kurt Russell"
        self.update_movie_data = "Jaws 3"

        assistant_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjMzUxN2VlMGYwMDAzZDhjZDExOSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc3OTYxNzYsImV4cCI6MTU5Nzg4MjU3NiwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiXX0.pFfDaOoCmC3z5I2AnI0yDL15Nai386wP9E9jqeybmHPs513BuE1MSv6-EdmbPcTOlaEEMR7GR6OMNsnr7CzyUOPT8618rQvT3LQBIcdbBaaCUT8Wum1LQG0uxTWjrIyDRwwQ9qkcgeGLR81u0EtlUSTzDN2JZGjVpeVW06NJp7vQid3N0uGh_lsSqhIJHUwqCQtrWV6WmFLxaL4vrnTTI9FadUrfdOPbu5qHc-YU17uYzzbBPzgb3G_jK6uEeuWozgkCfKEkFtNIeriQIIUsmFKwDZUN7IAzXSHnp-RcdaftnJOqH6q-OigP5WMzrTGrl-vdev1vnbviWl88iCpIsg"
        director_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjM2ZhZDJmMWNkMDAzN2VmZDg3NyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc3OTcyOTEsImV4cCI6MTU5Nzg4MzY5MSwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDptb3ZpZXMtZGV0YWlsIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.V84oeorA-66tffrNzgP1xT6ttVNp6g5AQeeE5vqS7mqddSmvNyn0bkkXAwGXVf1KrqRus8rbh8dPGYsTSxCIuBmmQKSkN3z5QzBrj7mb-29TbVEAQmbp0dShThWNX_r_gR-FLelTjyAQVmXOZ57Tsex3SSMIoWBAz0fjqdimf0J_HW_rIow_jAUHYrrt5EuaN5dN_NfZ_x4tPGGNRGJkQXeFsI2WgAXrU1ZX4ua3evQM1oqoXoekYkygB6208BTIKTZWi7hQWGJXdl2T2QqT1bvWhRyQXpPIi7Dd8XIuovp-RDzXqECL03Tp1tOYZuE6M54HVtBWp3jtb_wgDt9P5Q"
        producer_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjNDQ4N2Q4YTllMDAzNzcxNjlmZCIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc3OTc0NjYsImV4cCI6MTU5Nzg4Mzg2NiwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycy1kZXRhaWwiLCJnZXQ6bW92aWVzLWRldGFpbCIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.O3dexNJlqAefARkawj8Zbbs1hn5-zj2MrA-2OhmvT6tEBxSGzUx51jsVz2lzydaG2pvkLw0DdZlaBa4_eRE2ogjSCyqrtTXEnRk3j-O4F5Y0I7wIfnmWfZrfAI8Y6H-L9N3KkKEUYJB8C8tAePAjQqJfS-Gb2Bq-aorvsgCGId5neZ4lwb2IlLrpiIb5Qrq0RJhPOejdBQ_73xWgl11fujCfZO8Gvcb5-DSiO0TpMErqTUKYHvZOsGNHgRWZW_-ccRz_b_YPpBFm_SY9RCnHJe67LAQUgAbC94KdFdqmMjIg6eGeuZkByAfA5bQXcvxYovvxcGOuqsyrpveTqaXGxw"

        expired_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjM2ZhZDJmMWNkMDAzN2VmZDg3NyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTcwOTgwNTAsImV4cCI6MTU5NzEwNTI1MCwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.CSIWw2EmE-uCD0nSScQz2wwRsNtpROtpw8_-6Rd2-QTCekEzPRBeyveCSC98v9AZE3apocpWiZZ11DJTBM_56t-gK85r9q_buuhogpOTd2WpcG1y-pvOc_LdzTwhoX0HhDUyJz7qDg9_OOquIZnhbcuyQBxNc9vLymlTWNsXHYZ0VjZefRJ2XoGtpeyGH3MDrQowPy6HUXFEj64WUDP2HR7Q9lYm1Yv7i7duuPjef2iB9gq1NzuWh13M-gL1X3y4whizwT5FOF4Zoj3M39lyokuhitgy5wNcoTMkY_7lckMutoprjEjtfm6ZSq1RWVDuLDz8aRxqS9awP2yytaGflg"
        malformed_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

        self.header_full_access = {
            'Authorization': 'Bearer {}'.format(producer_access_jwt)
        }
        self.header_director_access = {
            'Authorization': 'Bearer {}'.format(director_access_jwt)
        }
        self.header_assistant_access = {
            'Authorization': 'Bearer {}'.format(assistant_access_jwt)
        }
        self.header_expired = {
            'Authorization': 'Bearer {}'.format(expired_jwt)
        }
        self.header_malformed = {
            'Authorization': 'Bearer {}'.format(malformed_jwt)
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
        #print(" ···· header ", self.header_full_access)
        res = self.client().get(
            "/actors-detail", 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actors"])

    # TODO: test for fail get /actors-detail

    def test_get_all_movies(self):
        res = self.client().get(
            "/movies-detail", 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movies"])

    # TODO: test for fail get /movies-detail

    def test_add_new_actor(self):
        res = self.client().post(
            "/actors", 
            json=self.new_actor, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["actor"])

    def test_400_if_new_actor_has_no_name(self):
        new_actor = {
            "age": 74,
            "gender": "Female"
        }
        res = self.client().post(
            "/actors", 
            json=new_actor, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_add_new_movie(self):
        res = self.client().post(
            "/movies", 
            json=self.new_movie, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["movie"])

    def test_400_if_new_movie_has_no_title(self):
        new_movie = {
            "release_date": ""
        }
        res = self.client().post(
            "/movies", 
            json=new_movie, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_update_actor(self):
        res = self.client().patch(
            "/actors/2",
            json={"name": self.update_actor_data}, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(actor.name, data["actor"]["name"])

    def test_404_if_update_actor_does_not_exist(self):
        res = self.client().patch(
            "/actors/10000",
            json={"gender": "Female"}, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_update_movie(self):
        res = self.client().patch(
            "/movies/2",
            json={"title": self.update_movie_data}, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(movie.title, data["movie"]["title"])

    def test_404_if_update_movie_does_not_exist(self):
        res = self.client().patch(
            "/movies/10000",
            json={"release_date": "01/01/0001"}, 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_delete_actor(self):
        print(" >>> test_delete_actor")
        res = self.client().delete(
            "/actors/1", 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(actor, None)

    def test_404_if_delete_actor_does_not_exist(self):
        print(" >>> test_404_if_delete_actor_does_not_exist")
        res = self.client().delete(
            "/actors/10000", 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_delete_movie(self):
        print(" >>> test_delete_movie")
        res = self.client().delete(
            "/movies/1", 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(movie, None)

    def test_404_if_delete_movie_does_not_exist(self):
        print(" >>> test_404_if_delete_movie_does_not_exist")
        res = self.client().delete(
            "/movies/10000", 
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")


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
