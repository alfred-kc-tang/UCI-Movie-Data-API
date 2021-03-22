import os
import json

from sqlalchemy import
from flask_sqlalchemy import SQLAlchemy

database_name = ""
database_path = "postgres://{}{}".format('localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):

class Actor(db.Model):