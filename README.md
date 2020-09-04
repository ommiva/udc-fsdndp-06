# Casting agency

## Introduction
Casting Agency application.

Simplify and streamline agency creation of movies and managing and assigning
actors to those movies.


## Getting started

### Pre-requisites

#### Backend

* Database

To create the database, first set DATABASE_URL environment variable

```bash
export DATABASE_URL=postgres://postgres@[host]:5432/[database_name]
```

(TODO: Remove example)
Example:   
```bash
export DATABASE_URL=postgres://postgres@localhost:5432/casting_agency
```

To start the database run
```bash
python manage.py db init
```

To create (or update) tables, run
```bash
python manage.py db migrate
python manage.py db upgrade
```



- - -
TODO: Remove debug

### DEBUG
* To install the application
```bash
$ pip install -r requirements.txt
```

* To run the application run the following command
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
or
```bash
$ FLASK_APP=flaskr FLASKNV=development flask run
```

- - -

The API is run on http://127.0.0.1:5000/ by default.

- - -

#### Testing
To run tests, run 
```bash
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting.sql
python test_app.py
```



### API Keys / Authentication
TODO: It requires no authentication at all.
The authentication system used for the project is Auth0.

#### Roles
- **Casting assistant**
  - Can view actors and movies.
- **Casting director**
  - Casting assistant permissions and...
  - Add or delete an actors from the database.
  - Modify actors or movies.
- **Executive Producer**
  - Casting director permissions and...
  - Add or delete an movies from the database.

#### Permissions
- **Casting assistant**
  - get:actors-detail
  - get:movies-detail
  - get:cast-detail
- **Casting director**
  - Casting assistant permissions plus...
  - post:actors
  - delete:actors
  - patch:actors
  - patch:movies
  - post:casting
  - delete:casting-actor
- **Executive Producer**
  - Casting director permissions plus...
  - delete:movies
  - post:movies
  - delete:casting-movies
- __Notes__
  - Any attempt to access endpoint without permission will result
    on a _403 \- Permission not found_ response.



### Errors

#### Response codes
- **200 - OK** – Everything is ok
- **201 - Created** - Resource created.
- **400 - Bad  request** – Client error.
- **401 - Unauthorized ^** – Missing or bad authentication.
- **403 - Forbidden ^** – User authenticated but not authorized to perform the requested operation.
- **404 - Not found** – The requested resource was not found.
- **405 - Method not allowed** – The requested method to access a
  resource was not allowed.
- **422 - Unprocessable** – The application can not procces the request.
- **500 - Internal server error** – Something went wrong. 

> **^ aknowledge** - From [stakoverflow](https://stackoverflow.com/questions/3297048/403-forbidden-vs-401-unauthorized-http-responses) 


#### Messages

```json
{
  "error": 400,
  "message": "Bad request",
  "success": false
}

{
  "error": 404,
  "message": "Resource not found",
  "success": false
}

{
  "error": 405,
  "message": "Method not allowed",
  "success": false
}

{
  "error": 401,
  "message": "Unauthorized",
  "success": false
}

{
  "error": 403,
  "message": "Forbidden",
  "success": false
}

{
  "error": 422,
  "message": "Unprocessable",
  "success": false
}

{
  "error": 500,
  "message": "Internal server error",
  "success": false
}
```

#### Authetication messages
```json
{
  "error": 400, 
  "message": "Permission not in JWT.", 
  "success": false
}

{
  "error": 401, 
  "message": "Authorization header is expected.", 
  "success": false
}

{
  "error": 401, 
  "message": "Token not found.", 
  "success": false
}

{
  "error": 401, 
  "message": "Authorization header MUST be bearer token.", 
  "success": false
}

{
  "error": 401, 
  "message": "Token expired.", 
  "success": false
}

{
  "error": 401, 
  "message": "Authorization malformed.", 
  "success": false
}

{
  "error": 401, 
  "message": "Incorrect claims. Please, check the audience and user.", 
  "success": false
}

{
  "error": 401, 
  "message": "Unable to parse atuhentication token.", 
  "success": false
}

{
  "error": 401, 
  "message": "Unable to find the appropiate key.", 
  "success": false
}

{
  "error": 403, 
  "message": "Permission not found", 
  "success": false
}
```



### Resource endpoint library

#### Actors

##### Endpoints

- GET /actors-detail
- [PATCH /actors/<int:actor_id>][patch-actors]
- DELETE /actors/<int:actor_id>
- POST /actors

###### GET /actors-detail
* Retrieves all actors available

* _Request arguments_
  * None

* _Response_
```json
{
  "actors": [
    {
      "age": 30,
      "gender": "Female",
      "id": 4,
      "name": "Emma Watson"
    },
    {
      "age": 78,
      "gender": "Male",
      "id": 1,
      "name": "Harrison Ford"
    },
    {
      "age": 81,
      "gender": "Male",
      "id": 7,
      "name": "Ian McKellen"
    },
    {
      "age": 69,
      "gender": "Female",
      "id": 6,
      "name": "Lynda Carter"
    }
  ]
}
```

* _CURL_
```
curl http://127.0.0.1:5000/actors-detail
```


[patch-actors]: (###### PATCH /actors/<int:actor_id>)
* Updates actor data for given actor id.

* _Request arguments_
  * Actor id
  * Optional (json)
    * Name
    * Age
    * Gender [Male / Female]

* _Response_
```json
{
  "actor": {
    "age": 58,
    "gender": "Male",
    "id": 2,
    "name": "Russell Crowe"
  },
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/actors/3 -X PATCH -H "Content-Type: application/json" -d '{"name":"Russel Crowe", "age": 58, "gender": }'
```


###### DELETE /actors/<int:actor_id>
* Deletes a actor given actor id.

* _Request arguments_
  * Actor id

* _Response_
```json
{
  "delete": 4,
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/actors/4 -X DELETE
```


###### POST /actors
* Creates an actor in the actors list, given his/hers name, gender and age.
* _Request arguments_
  * Name
  * Gender
  * Age

* _Response_
```json
{
  "actor": {
    "age": 43,
    "gender": "Male",
    "id": 9,
    "name": "Michael Fassbender"
  },
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"name":"Michael Fassbender", "age":43, "gender":"Male"}'
```




#### Movies

##### Endpoints

- GET /movies-detail
- PATCH /movies/<int:movie_id>
- DELETE /movies/<int:movie_id>
- POST /movies

###### GET /movies-detail
* Retrieves all movies available

* _Request arguments_
  * None

* _Response_
```json
{
  "movies": [
    {
      "id": 6,
      "release_date": "11/28/2003",
      "title": "Kill Bill: Volume 1"
    },
    {
      "id": 1,
      "release_date": "07/14/2008",
      "title": "The Dark Knight"
    },
    {
      "id": 5,
      "release_date": "01/30/1991",
      "title": "the silence of the lambs"
    }
  ]
}
```

* _CURL_
```
curl http://127.0.0.1:5000/movies-detail
```


###### PATCH /movies/<int:movie_id>
* Updates movie data for given movie id.

* _Request arguments_
  * Movie id
  * Optional (json)
    * Title
    * Release date

* _Response_
```json
{
  "movie": {
    "id": 2,
    "release_date": "09/09/2020",
    "title": "Krull"
  },
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/movies/3
```


###### DELETE /movies/<int:movie_id>
* Deletes a movie given movie id.

* _Request arguments_
  * Movie id

* _Response_
```json
{
  "delete": 4,
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/movies/4 -X DELETE
```


###### POST /movies
* Creates a movie in the movies list, given a title and release date.
* _Request arguments_
  * Title
  * Release date

* _Response_
```json
{
  "movie": {
    "title": "The Good, the Bad and the Ugly",
    "release_date": "12/23/1966"
  },
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title": "The Good, the Bad and the Ugly", "release_date": "12/23/1966"}'
```




#### Casting

##### Endpoints

- GET /cast-detail
- PATCH /cast/<int:movie_id>
- DELETE /cast/<int:cast_id>
- DELETE /cast-movie/<int:movie_id>
- POST /cast


###### GET /cast-detail
* Retrieves all movies available.

* _Request arguments_
  * None

* _Response_
```json
{
  "cast": [
    {
      "actor_id": 7,
      "actor_name": "Ian McKellen",
      "movie_id": 7,
      "movie_release_date": "06/18/1993",
      "movie_title": "Last Action Hero"
    }
  ]
}
```

* _CURL_
```
curl http://127.0.0.1:5000/cast-detail 
```


###### POST /cast
* Adds new movie-actor assignation.

* _Request arguments_
  * Actor (id)
  * Movie (id)

* _Response_
```json
{
  "cast": {
    "actor_id": 4,
    "actor_name": "Emma Watson",
    "movie_id": 4,
    "movie_release_date": "12/25/2019",
    "movie_title": "Little Women"
  },
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/cast  -X POST -H "Content-Type: application/json" -d '{"actor": 4, "movie": 4}'
```


###### DELETE /cast/<int:cast_id>
* Deletes existing movie-actor assignation.

* _Request arguments_
  * Cast (id)

* _Response_
```json
{
  "delete": {
    "actor_id": 8,
    "actor_name": "Jodie Foster",
    "movie_id": 5,
    "movie_release_date": "01/30/1991",
    "movie_title": "the silence of the lambs"
  },
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/cast/2  -X DELETE
```


###### DELETE /cast-movie/<int:movie_id>
* Deletes existing movie and all its assignations.

* _Request arguments_
  * Movie (id)

* _Response_
```json
{
  "delete": 2,
  "success": true
}
```

* _CURL_
```
curl http://127.0.0.1:5000/cast-movie/8  -X DELETE
```




### Authors

Omar Miramontes

### Acknowledgement

Udacity team
