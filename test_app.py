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
            + "nIwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc2"\
            + "5kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjMzUx"\
            + "N2VlMGYwMDAzZDhjZDExOSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOj"\
            + "E1OTg2NDU1MzIsImV4cCI6MTU5ODczMTkzMiwiYXpwIjoidjEzcEZiQlBPbHZo"\
            + "TmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIj"\
            + "pbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmNhc3QtZGV0YWlsIiwiZ2V0Om1v"\
            + "dmllcy1kZXRhaWwiXX0.J-jaEx-e4xvaz8JrL5LKfpIH4C6-Kwoj7kA1tGzrMC"\
            + "8r2C9uR7iO9pJo-Q_uL8UHOVKyQzBhSl4F4HZsUsALtyl_feKhxxeBvrXBeKag"\
            + "CgPAmAtT7Qt68Z52auQ9LvqXkuHEpV4jyCwAkH8Nw_OO_ixqJ0jhGLhDDsybvK"\
            + "xgqyxSgM4nLkN_WR-51TkUAwXHfo5Ly3_VWxBVjFVockEkkWQIBA-uCtYgF02V"\
            + "sfEp83NPKUv3EZ49QoacnF0JrT10BzpXXG1WnjTsD0uBHABWGxrJnpJBpM6Dtk"\
            + "XEnGoXaCqRmGE_uSx4xu64JRyostH66-Vge9Xqo6Gfnsu7IzcAow"

        director_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25"\
            + "kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjM2ZhZ"\
            + "DJmMWNkMDAzN2VmZDg3NyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE"\
            + "1OTg2NDkwNzgsImV4cCI6MTU5ODczNTQ3OCwiYXpwIjoidjEzcEZiQlBPbHZoT"\
            + "mR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjp"\
            + "bImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDpjYXN0L"\
            + "WRldGFpbCIsImdldDptb3ZpZXMtZGV0YWlsIiwicGF0Y2g6YWN0b3JzIiwicGF"\
            + "0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0OmNhc3RpbmciXX0.FojMF"\
            + "6akenAXZWhhP2aPRqBYDUyGQpDwnSq5WLNMbqCGLakBBhFCYym4mBZ24TN-tzT"\
            + "33CQWC_oHMhBWRan22QdmPsuuc9dwfQqzUaMfhJCp1BhTJiQ5P9n5gKFSgc0Q1"\
            + "7Q9guj9BN7aDjyPAw-gf1Z8mKKJpnLBXw_vqm0XuFC9f--tV060euhjOGuW2cp"\
            + "jLm7ClnhvRrOF5X6KgkfSfrMUNnJh6zB2nozYOQV7LbrIrMqijpBiSSqP5M9Cy"\
            + "H_1kCPZhNMWLluCAp10c0t1-5Sf9ResqBqCROlvc4yELHjZo0StNRlgKD7iCrp"\
            + "skbWVuITBC-HhHwKsDMCsJ1kvVg"

        producer_access_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6In"\
            + "IwVzRteHBqWUJIaW9JR0dBZ2xSbiJ9.eyJpc3MiOiJodHRwczovL29tdi1mc25"\
            + "kLWNhc3RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzFjNDQ4N"\
            + "2Q4YTllMDAzNzcxNjlmZCIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE"\
            + "1OTg2NDkyMTUsImV4cCI6MTU5ODczNTYxNSwiYXpwIjoidjEzcEZiQlBPbHZoT"\
            + "mR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjp"\
            + "bImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycy1kZ"\
            + "XRhaWwiLCJnZXQ6Y2FzdC1kZXRhaWwiLCJnZXQ6bW92aWVzLWRldGFpbCIsInB"\
            + "hdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zd"\
            + "DpjYXN0aW5nIiwicG9zdDptb3ZpZXMiXX0.EoC_pfBMh8czoNi4rU1lYl7HasU"\
            + "X9Cmcmhq4LvxgJHEb9oddKXvGQ68atJPNb2bjJbkNEO7HKgxR7N-FHgQ98_2x3"\
            + "nZ02tkJt8ktCdMHCz6uOxVyXatbMFiUDOMPxgYdlVjnZtfo_cXF2uP4BN-9iPA"\
            + "0WXveaPnJaBhAPVVY7D1joKXg6_TRbQp7Oh8EQAnU_gGlqn2c4g8H-425oJVhw"\
            + "4tuyov507qK1584x1SO8FIS-z15a996Cnq-YphjKawx1Q2I_bMd0ogJYRPzaqr"\
            + "tzOpG0libF31LT4ui_4bfi_UBocaGnBfkMJue1ZwOkarR5mkXHsrqzgkauT0Wn"\
            + "gCj4Q"

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
            + "E1OTg2NDQxOTAsImV4cCI6MTU5ODczMDU5MCwiYXpwIjoidjEzcEZiQlBPbHZ"\
            + "oTmR2bXNzNlFMZTEzTDJncHo5VG8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25z"\
            + "IjpbImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0OmFnZW50LWRldGFpbCJdfQ.c3"\
            + "491jC-Ab8EQOc1lk_cK9AetivNymxxDEJY28lCD53_r_wHotvxVAtedw3qHKB"\
            + "sb1w98IOd0GB2ohfwdRa2vQcvFHh3vC3_QZpekms6YQ2gFOmDBEp0rWfL7m5z"\
            + "B-I5Lc9rezVpGWNk0qHl69YdZuNVgoGduDRm7jGrq04xW7vji0GfnPCIf0zvi"\
            + "P3xzgRZesF1PcG9DDPWSwLBnQ-CCBxojE1nqAPRa_zgBcTd5iLmhuR5nxULfR"\
            + "oxASXZXc4F8eFNcGssttW2i2zN4RifQzvBGMStbLphTKSTqyidVprAhFohAZR"\
            + "n0tjA_IL7PEq8-GH6mK-EDsrMDOiIpGytcA"

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
        print("test_401_if_get_all_cast_incorrect_calims")
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
