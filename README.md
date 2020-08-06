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



-------------------------------
TODO: Remove debug
-------------------------------
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

The API is run on http://127.0.0.1:5000/ by default.
===============================


## Testing
To run tests, run 
```bash
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting.sql
python test_app.py
```