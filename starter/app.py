import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#from models import

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)

  # Set up CORS that allows any origins for the api resources
  cors = CORS(app, resources={r"/api/*": {"origin": "*"}})

  # Set Access-Control-Allow headers and methods
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)