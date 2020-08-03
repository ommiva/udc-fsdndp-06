
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date, ForeignKey

import json
import os

db_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
  '''
  Movie
  '''

  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }

  def __repr__(self):
    return f'<Movie {self.id} "{self.title}">'


class Actor(db.Model):
  '''
  Actor
  '''

  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String(15))

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender
  
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()
  
  def delete(self):
    db.session.add(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }
  
  def __repr__(self):
    return f'<Actor {self.id} "{self.name}" [a:{self.age}, g:{self.gender}]>'


class Cast(db.Model):
  '''
  Actors assigned to Movies
  '''

  __tablename__ = 'movie_cast'

  id = Column(Integer, primary_key=True)
  actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
  movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

  def __repr__(self):
    return f'<Cast {self.id} actor: {self.actor_id} movie: {self.movie_id}>'


