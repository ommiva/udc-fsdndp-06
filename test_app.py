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
            + "nIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc2"\
            + "5kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjMzUx"\
            + "N2VlMGYwMDAzZDhjZDExOSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOj"\
            + "E2MDA3MDU2NjQsImV4cCI6MTYwMDc5MjA2NCwiYXpwIjoidjEzcEZiQlBPbHZo"\
            + "TmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIj"\
            + "pbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1v"\
            + "dmllcy1kZXRhaWwiXX0.u8LRWdiYstK-TV7z-R6TbQhZzwYjM8myQxVmgQ2Kqi"\
            + "0Fdivx_Yr1o3kf8hG5j4rgGoJcZ0vtAo7ba4VukkFkrNx4lodpwUfEDZtCBRjl"\
            + "GGbCQvgC1jtsAg0yA--0QN0jMiyfRHesaEe6AXOHl73yGmfBI9k33N2v-rtHWD"\
            + "OkaNC8i1rC7YYwBnmFVOuRjZPDdOea7XU95J86pIWkIv7KnrVr9h8r-E5nIhis"\
            + "0oUK5gvviXa1fpa7JCRwJalGFhzG5m6GOYvpnFxkosngHkmARW1hmQtGv5__OV"\
            + "eRbT4SbJE-JVe-TuZH7-bj5rFJq0kzhkEFEaKXGiOpYxZBrPOa3Q"

        director_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25"\
            + "kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjM2ZhZ"\
            + "DJmMWNkMDAzN2VmZDg3NyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE"\
            + "2MDA3MDU4NTcsImV4cCI6MTYwMDc5MjI1NywiYXpwIjoidjEzcEZiQlBPbHZoT"\
            + "mR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjp"\
            + "bImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZy1hY3RvciIsImdldDphY"\
            + "3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXR"\
            + "haWwiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9yc"\
            + "yIsInBvc3Q6Y2FzdGluZyJdfQ.S872a-haJZXatPLlV3pC9C7my3pN2KpcMLli"\
            + "-FrzkDB_B6GoElVYhc5mIVJC6wLFsG-IXgQ-P_xM3XMxnXfUcC0m8MBjwYSjTV"\
            + "_owGKkEZT7lc-l4e-YrOwo8aK99BtiHF00z-TcbVGvvCHHFiVdl38TRSrpsK5_"\
            + "6W1nFbhT42OqfHJ3u_rdKyC-5ZkI4Ci7EMeOdkuj-FynUO2aTPFpWOUa7fn87Z"\
            + "vz7rxarYJcNrUNYDxw7AoeDyX88VA8Kbni4UScBr-03I85WZmgeI6WSsL1EyNK"\
            + "4Nplp9IX-ulaSCPoH80KAvH1y17_jLX3gQlEJ51D9OHtdLcl4cuvx8KIuw"

        producer_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25"\
            + "kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjNDQ4N"\
            + "2Q4YTllMDAzNzcxNjlmZCIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE"\
            + "2MDA3MDYwOTQsImV4cCI6MTYwMDc5MjQ5NCwiYXpwIjoidjEzcEZiQlBPbHZoT"\
            + "mR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjp"\
            + "bImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZy1hY3RvciIsImRlbGV0Z"\
            + "TpjYXN0aW5nLW1vdmllIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMtZGV"\
            + "0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiLCJwY"\
            + "XRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q"\
            + "6Y2FzdGluZyIsInBvc3Q6bW92aWVzIl19.H2GS4zpHNqvXqjdCtIctGZj1VfoV"\
            + "o1FCjT72uYsExtWXLTIh9QHa6HPOR3N41SU_DDDODvA8NjFs4eSRQPsJEfAV7d"\
            + "JDVfZVbpzKqeieKSbfFTTePyDNIAeo1luNq-Ls7i7hmpji7x_JfO039QyVxopw"\
            + "SynunBmu4Zzk6G8S8ITMz6UnfU_hq8axdZeeXHpKP6IuOfJenPhyDyD4k6NjTv"\
            + "VXaINB9Ek-GQgH1TP0fdCuCc7yZJW495Twn0TcA2rB-Dlkm1o_NrcMol00DmgZ"\
            + "eM3qY7Pej_Bk_OD-G43AOrwhGBCqeKehOPc8zy04ge8HYqojdaIgf-zVnVQQn7"\
            + "_dlA"

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
            + "VzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25k"\
            + "LWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDdlM2RmO"\
            + "WM1MTA2MDA2ZGUxNmMxOSIsImF1ZCI6ImNhc3RpbmdhZ2VudHMiLCJpYXQiOj"\
            + "E2MDA3MDY3NDMsImV4cCI6MTYwMDc5MzE0MywiYXpwIjoidjEzcEZiQlBPbHZ"\
            + "oTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25z"\
            + "IjpbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmFnZW50LWRldGFpbCJdfQ.w0"\
            + "A-ZM3FVAXLFqTdjmolsIGfncfrahFsBjR8aFgnkjcWMj4d_cZa5aGSIlY2rIM"\
            + "C8K_LqFaK-qKDA9yHD8akg3Q6CfFvI70-jSHq0HhHbdIeh2c-uWqCTCDdcy8e"\
            + "jwFrALFLjFQrd6Al9D2gWR6yMwTDNbLepdZty9M70-0hNcc58Ibguaib4XCZ1"\
            + "oUM6MurAYNTLREmUN1RvgD4GBaWXZ7_9rvEgrefEKNC1YK9IEnn0GtmNNLNdX"\
            + "iVUbWb8vxvGyJplaWaJFb3XiAcg99nTVCQFbl7NITKyA7jt8Kjivqw33L7yPI"\
            + "mZzpO9Q52jZvI1zikkPEi0SJXBSMyNOzt8A"

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
