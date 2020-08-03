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
