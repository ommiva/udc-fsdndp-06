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

        self.total_filtered_empty = 0

        assistant_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6I"\
            + "nIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjMzUxN2VlMGYwMDAzZDhjZDExOSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTkxNDczNTMsImV4cCI6MTU5OTIzMzc1MywiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiXX0.Sqv2MA7k6RNo8taHHrPlxGC2A3muAKSc8LKYEVQt7PRJy9Xs5sPbTbphXFNCvT30rqzUDfLo03j7bCcX-85LtD7BkcHRlZjSrqG3phzFFvRaey48LJ6hbiTOtSFeR5QTQbVxZ8ir6awtqAfXZV8magaEBn86NQZJdFuy42bT6qxC4x9fGPksYVIXWSjFG_uhFon4S2wdCr1ezxC-78AiY2BGHxsU9juSz805zby6OiLx1fqhOUwoSLP-gPT5NlF43mRwizNs4bgUy9OWxUZHNcXMovMNObIQx97Du4bzIWu93u8gzL4oFFI1s64kFF8um57I1TmFM0ims2vea_q1zA"

        director_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjM2ZhZDJmMWNkMDAzN2VmZDg3NyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTkxNDc0MzcsImV4cCI6MTU5OTIzMzgzNywiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZy1hY3RvciIsImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y2FzdGluZyJdfQ.XvSh01LuH2hYyBJe2dkVdpKjOoBcPetPly8XbQ5cwsoKgnHa2-vxJuWpFN3Qzb4yxje64Ejjedh65IeoElDpfNTBNdDYDmG4bDb7g2grAOyA3fM_H5K-c23nTWJzhi7LLnpi2YAR-bJMzOiM23yDGlhZMP6LHRoxBJGNLlymR7vniRIi6kU0xDIzxV_4QK3QdIIrfWx3WOZ2-_3dhZcARVJa0ODyFKr0qFTV1K_UUzRc4e4JoR337awG1hlh8kPYYRkYesl7nsiTMxOEzo2lceCLWQisqYBoTzFFbNWs1K0-y6IqrQ9n6fUqZwzgICJSBHJ6Dr1lcV6EANPHxS8dYA"

        producer_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjNDQ4N2Q4YTllMDAzNzcxNjlmZCIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTkxNDc1NjQsImV4cCI6MTU5OTIzMzk2NCwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZy1hY3RvciIsImRlbGV0ZTpjYXN0aW5nLW1vdmllIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y2FzdGluZyIsInBvc3Q6bW92aWVzIl19.cy2nq7kYKSy-_7neCbfgrA-V_ZTXdu-qb-b0RhDvlgTBoNJDBHPBBszawaDppSgFFlKae5ykyWbcMR3-KuMHhJWveQiaGQVO15OoPBoCXvUY0qhwQQ6sJOCaAg9PbrxPKWE_gGVbpvL7Dg5vAMj-7DIG5oOOku32sNwWLkViMFAugH6iro2GCqtDvvGQAlk7EPwDZo1vw7_dRInhi8k7Bt_fNKXYHgPtX9MOr_-aVqp4HImTD0F5i3LsKrzDYurATl9OPvA4_lXrXxBlxYPVJqW1HNGM_o285jxOsPzDeFUR8Oe_QmCH-nulei7z0AAXOmBHEVpSTYdYBWTNb5jpMA"

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
            + "VzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDdlM2RmOWM1MTA2MDA2ZGUxNmMxOSIsImF1ZCI6ImNhc3RpbmdhZ2VudHMiLCJpYXQiOjE1OTkxNDcyMzksImV4cCI6MTU5OTIzMzYzOSwiYXpwIjoidjEzcEZiQlBPbHZoTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmFnZW50LWRldGFpbCJdfQ.qYVRknmrexNXM1JjpcRq-ncZK0nQYlnvqTNXZmv-vVUHNVL5qWC4dYLNMJChA2-1JYlJPO30-OuyaVh32cT_hSTZ-xI6CtBKqq1LWAslDBdhF9YnPRaXnr6UPq-qSKSUgK8ebuHbsugBtigmx4I-MvLAj2nMLb-hUB5Bx8qedvol5_rRJKiFGfEGd417HR4TBRkVcpSmDGJX5VDolgegIYgpHJYuvfa4v9VEuE0jcr5dOUs4U3oiyMZ7IoywrAtlDPuQ0sR-S5HL-Ft6R3_6-oVqZYhQJNA94sBo8Ucyf0t8U_c9fjtYMnMk4_-AkI-A45hZGIBZIAFEwi2pRSmqJA"

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
        self.assertEqual(total_cast, self.total_filtered_empty)

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
        self.assertEqual(total_cast, self.total_filtered_empty)

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

    def test_delete_cast_movie(self):
        print(" >>> test_delete_cast_movie")
        # print("To delete: ", Cast.query.filter_by(movie_id=8).count())
        res = self.client().delete(
            "/cast-movie/8",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        total_found = Cast.query.filter_by(movie_id=8).count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_found, self.total_filtered_empty)

    def test_404_if_delete_cast_movie_not_found(self):
        print(" >>> test_deleted_cast_movie_not_found")
        res = self.client().delete(
            "/cast-movie/8000",
            headers=self.header_full_access)
        data = res.get_json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_404_if_delete_cast_movie_has_no_movie_id(self):
        print(" >>> test_delete_cast_movie_has_no_movie")
        res = self.client().delete(
            "/cast-movie/",
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
        .filter(Cast.id == 6)\
        .one_or_none()
    if deleted_cast is None:
        cast = Cast(actor_id=1,
                    movie_id=2)
        cast.id = 6
        cast.insert()

    deleted_cast = Cast.query\
        .filter(Cast.id == 7)\
        .one_or_none()
    if deleted_cast is None:
        cast = Cast(actor_id=2,
                    movie_id=1)
        cast.id = 7
        cast.insert()


# Mtext executable
if __name__ == "__main__":
    unittest.main()
