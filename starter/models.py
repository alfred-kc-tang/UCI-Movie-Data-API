import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_cors import CORS

database_name = "film"
database_path = "postgres://{}/{}".format('postgres@localhost:5432', database_name)

db = SQLAlchemy()

# Initialize flask app.
def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    # Set up CORS that allows any origins for the api resources
    cors = CORS(app, resources={r"/api/*": {"origin": "*"}})
    moment = Moment(app)

    # Set Access-Control-Allow headers and methods
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    return app

# Conncet app and database.
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    return db
    #db.init_app(app)
    #db.create_all()

# Create model for movie.
def setup_movie_model(db):
    class Movie(db.Model):
        __tablename__ = 'Movie'
        
        id = db.Column(db.String, primary_key=True, nullable=False)
        title = db.Column(db.String(500))
        year = db.Column(db.String(120))
        director = db.Column(db.String(120))
        actors = db.relationship("Actor", backref="movie")
    return Movie

# Create model for actor.
def setup_actor_model(db):
    class Actor(db.Model):
        __tablename__ = 'Actor'
        
        id = db.Column(db.Integer, primary_key=True, nullable=False)
        film_id = db.Column(db.String, db.ForeignKey('Movie.id'), nullable=False)
        name = db.Column(db.String(120))
        character_type = db.Column(db.String(120))
    return Actor 
