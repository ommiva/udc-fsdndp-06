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

        assistant_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6I"\
            + "nIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjMzUxN2VlMGYwMDAzZDhjZDExOSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTkwODUwNTcsImV4cCI6MTU5OTE3MTQ1NywiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiXX0.vr3lEU3qwWA8veurN9KKLiu0-ozYBn0gq1YkNMeNbt2ZyMUvqTC45egr6aFEcN7ef8n7_x-Wfbam1CPRk71kcPicizJgIu_RA7dRWqadTr1dyXBNOX5G7XgnEoO3GFrjydt8isgCzpwHXxgHA2TT2FPKtSkFkcYUg465aZf0rd0FbpM6vyfDyJHnhGa8t2WCgLpxWLnPByMROZKNZg0CqTSc994K9K0fthNI8_oJvEsuuY-nx1rXGzY_vJs5jhqxyhe0RrDHyLupv6PnX0TPiPourk3jWU4ZHuAbi_GTGey5tBfIMs1qddqSwhi0EEQM3Hld1dau7C_iraMsGmsNyQ"

        director_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjM2ZhZDJmMWNkMDAzN2VmZDg3NyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTkwODUxMTcsImV4cCI6MTU5OTE3MTUxNywiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZy1hY3RvciIsImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y2FzdGluZyJdfQ.w9rhryKJLQRgP6i-E95D0C6hKv9nJlJtfPq4nPQQz1Y4VeMWtNU0PjYRiM5VJb0c3KC6ARYideqYGtYA_BhLXvJqFwRuwfEi8BxKFZ3ZlEKxDpXKrKKJwU7huowyCQaAdqARDMswytAbpknYBt66iHhiu-X7lNrVoJLR72w4ibWR8ZAQdC3XdhVnn113zvT7Ur0D9J-Byr6B442TCtjpxQBAng8aame9UA88gqn4f1OOcA3xFiWwraiwJbsaovTKl_Iz2oGDkWRcdi620m2vj7dQKSW5Kc09w7cpjGDXtvZleoLIFlkrAZOOfDBk_dVB6GkH-Yi5Fx_XrBztGEKkyg"

        producer_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjNDQ4N2Q4YTllMDAzNzcxNjlmZCIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTkwODUyMTUsImV4cCI6MTU5OTE3MTYxNSwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZy1hY3RvciIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDpjYXN0LWRldGFpbCIsImdldDptb3ZpZXMtZGV0YWlsIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0OmNhc3RpbmciLCJwb3N0Om1vdmllcyJdfQ.d2kmvqOws48JynjSZdubK5RoPY0YBrgeJ1Vvw9tzSxoyDJPldfDJXfyc5MQSpo4Wa3FCrMkJ_ey2sf3rmJdmINpFs8W72luFDElFcdGgJARZhBZW3ZL-Co7NXOTH12EEX8WSupj0yDi_3qreA2vIzBxeY_IO2QKSdBDffDLOy5T_i6_-D24de1x3JI2u9a6ETgWCC--1QVhs1QZB6C1CAwOF2UIp8aiIbwp5DVHufM03XvTT45ixgEFR-XJHQsDNBQeb7wpBnHGT1xBPcV3NovX9Z9rrUo6XzQ62iz6yoOmil8SG2PguIHhnLWeyhonmPJJtQfsoxdClIgxMqxRoQw"

        expired_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIwVzRteH"\
            + "BqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3R"\
            + "pbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjM2ZhZDJmMWNkM"\
            + "DAzN2VmZDg3NyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTcwOTg"\
            + "wNTAsImV4cCI6MTU5NzEwNTI1MCwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzN"\
            + "lFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV"\
            + "0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjd"\
            + "G9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.CSIWw2EmE-uCD0"\
            + "nSScQz2wwRsNtpROtpw8_-6Rd2-QTCekEzPRBeyveCSC98v9AZE3apocpWiZZ1"\
            + "1DJTBM_56t-gK85r9q_buuhogpOTd2WpcG1y-pvOc_LdzTwhoX0HhDUyJz7qDg"\
            + "9_OOquIZnhbcuyQBxNc9vLymlTWNsXHYZ0VjZefRJ2XoGtpeyGH3MDrQowPy6H"\
            + "UXFEj64WUDP2HR7Q9lYm1Yv7i7duuPjef2iB9gq1NzuWh13M-gL1X3y4whizwT"\
            + "5FOF4Zoj3M39lyokuhitgy5wNcoTMkY_7lckMutoprjEjtfm6ZSq1RWVDuLDz8"\
            + "aRxqS9awP2yytaGflg"

        malformed_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMj"\
            + "M0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."\
            + "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

        claims_error_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIw"\
            + "VzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDdlM2RmOWM1MTA2MDA2ZGUxNmMxOSIsImF1ZCI6ImNhc3RpbmdhZ2VudHMiLCJpYXQiOjE1OTkwODUyODEsImV4cCI6MTU5OTE3MTY4MSwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmFnZW50LWRldGFpbCJdfQ.VsHU_PU_J7PQPAoMV25qH2iGC3WHXwndgPWWdvoZ3isqtOO7c587vEWQY4WDpiTkcsQV0DyYj4Ydn3Xwm1EPswp9dtrk2KxC2XqB87Tr6feBs3pdRxqWkiPH-QjaZhgaNnS1qhckLE-Fo1p-i2y84UGkvIWq3NNdge3hBUaK3N4BfpBYIEn23CNsIrcX7H_8FtRSJrafkI_StgjILd7tpN9pvzsvFSdmR7P_ybTCqi3JkSz5SWtArrrQOA6hVlWOjnvsGFcf-0fJufak4ga1OYDAQtR_BdA-YqJPRqaUL3qwEeaiIk1ONjX2deByt6mfTbOXR79Tm9JmuFa5lHk6lA"

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
        self.header_claims = {
            'Authorization': 'Bearer {}'.format(claims_error_jwt)
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
        # print(" ···· header ", self.header_full_access)
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
        print(" >>> test_400_if_new_actor_has_no_name")
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

    def test_403_if_add_new_actor_has_no_permission(self):
        print(" >>> test_403_if_add_new_actor_has_no_permission")
        res = self.client().post(
            "/actors",
            json=self.new_actor,
            headers=self.header_assistant_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found")

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
        print(" >>> test_400_if_new_movie_has_no_title")
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

    def test_403_if_add_new_movie_has_no_permission(self):
        print(" >>> test_403_if_add_new_movie_has_no_permission")
        res = self.client().post(
            "/movies",
            json=self.new_movie,
            headers=self.header_director_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found")

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
        print(" >>> test_404_if_update_actor_does_not_exist")
        res = self.client().patch(
            "/actors/10000",
            json={"gender": "Female"},
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_404_if_update_actor_access_expired(self):
        print(" >>> test_404_if_update_actor_access_expired")
        res = self.client().patch(
            "/actors/1",
            json={"gender": "Female"},
            headers=self.header_expired)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Token expired.")

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
        print(" >>> test_404_if_update_movie_does_not_exist")
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
        total_cast = Cast.query.filter_by(actor_id=1).count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(actor, None)
        self.assertEqual(total_cast, 0)

    def test_404_if_delete_actor_does_not_exist(self):
        print(" >>> test_404_if_delete_actor_does_not_exist")
        res = self.client().delete(
            "/actors/10000",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_403_if_delete_actor_has_no_permission(self):
        print("test_403_if_delete_actor_has_no_permission")
        res = self.client().delete(
            "/actors/1",
            headers=self.header_assistant_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found")

    def test_delete_movie(self):
        print(" >>> test_delete_movie")
        res = self.client().delete(
            "/movies/1",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()
        total_cast = Cast.query.filter_by(movie_id=1).count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(movie, None)
        self.assertEqual(total_cast, 0)

    def test_404_if_delete_movie_does_not_exist(self):
        print(" >>> test_404_if_delete_movie_does_not_exist")
        res = self.client().delete(
            "/movies/10000",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_403_if_delete_movie_has_no_permission(self):
        print(" >>> test_404_if_delete_movie_has_no_permission")
        res = self.client().delete(
            "/movies/1",
            headers=self.header_director_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found")

    def test_get_all_cast(self):
        print(" >>> test_get_all_cast")
        res = self.client().get(
            "/cast-detail",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["cast"])

    def test_401_if_get_all_cast_incorrect_calims(self):
        print(" >>> test_401_if_get_all_cast_incorrect_calims")
        res = self.client().get(
            "/cast-detail",
            headers=self.header_claims)
        data = res.get_json(res.data)

        message = "Incorrect claims. Please, check the audience and user."

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], message)

    def test_add_new_cast(self):
        res = self.client().post(
            "/cast",
            headers=self.header_full_access,
            json={"movie": 4, "actor": 4})
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["cast"])

    def test_fail_if_new_cast_has_no_movie(self):
        res = self.client().post(
            "/cast",
            headers=self.header_full_access,
            json={"actor": 4})
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_fail_if_new_cast_has_no_actor(self):
        res = self.client().post(
            "/cast",
            headers=self.header_full_access,
            json={"movie": 4})
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_fail_if_new_has_actor_not_found(self):
        res = self.client().post(
            "/cast",
            headers=self.header_full_access,
            json={"movie": 4, "actor": 1000})
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
    
    def test_delete_cast_actor(self):
        print(" >>> test_delete_cast_actor")
        res = self.client().delete(
            "/cast/4",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        cast = Cast.query.filter(Cast.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(cast, None)

    def test_404_if_delete_cast_actor_has_no_cast(self):
        print(" >>> test_404_if_delete_cast_actor_has_no_cast")
        res = self.client().delete(
            "/cast/",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_404_if_delete_cast_actor_not_found(self):
        print(" >>> test_404_if_delete_cast_actor_not_found")
        res = self.client().delete(
            "/cast/4000",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
    
    # def deleted_cast_movie(self):




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
    
    deleted_cast = Cast.query\
        .filter(Cast.id == 2)\
        .one_or_none()
    if deleted_cast is None:
        cast = Cast(actor_id=8,
                    movie_id=5)
        cast.id = 2
        cast.insert()
    
    deleted_cast = Cast.query\
        .filter(Cast.id == 3)\
        .one_or_none()
    if deleted_cast is None:
        cast = Cast(actor_id=3,
                    movie_id=6)
        cast.id = 3
        cast.insert()
    
    deleted_cast = Cast.query\
        .filter(Cast.id == 4)\
        .one_or_none()
    if deleted_cast is None:
        cast = Cast(actor_id=8,
                    movie_id=8)
        cast.id = 4
        cast.insert()
    
    deleted_cast = Cast.query\
        .filter(Cast.id == 9)\
        .one_or_none()
    if deleted_cast is None:
        cast = Cast(actor_id=1,
                    movie_id=2)
        cast.id = 9
        cast.insert()
    
    deleted_cast = Cast.query\
        .filter(Cast.id == 10)\
        .one_or_none()
    if deleted_cast is None:
        cast = Cast(actor_id=2,
                    movie_id=1)
        cast.id = 10
        cast.insert()


# Mtext executable
if __name__ == "__main__":
    unittest.main()
