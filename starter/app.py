import os
import json

from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import create_app, setup_db, setup_movie_model, setup_actor_model

# app config
app = create_app()
db = setup_db(app)
migrate = Migrate(app, db)

# models
Movie = setup_movie_model(db)
Actor = setup_actor_model(db)

# pagination
items_per_page = 100
def paginate_results(request, items):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * items_per_page
  end = start + items_per_page
  current_items = items[start:end]
  return current_items

# controllers
@app.route('/movies', methods=['GET'])
def get_movies():
  page = request.args.get('page', 1, type=int)
  movies = Movie.query.all()
  if len(movies) == 0:
    abort(404)
  else:
    paginated_movies = Movie.query.order_by(
      Movie.year).paginate(page=page, per_page=items_per_page).items
    
  return jsonify({
    'success': True,
    'movies': {movie.id: {
      'title': movie.title,
      'year': movie.year,
      'director': movie.director} for movie in paginated_movies}
  })

@app.route('/actors', methods=['GET'])
def get_actors():
  page = request.args.get('page', 1, type=int)
  actors = Actor.query.all()
  if len(actors) == 0:
    abort(404)
  else:
    paginated_actors = Actor.query.order_by(Actor.id).paginate(
      page=page, per_page=items_per_page).items
  
  return jsonify({
    'success': True,
    'actors': {actor.id: {
      'name': actor.name,
      'film_title': actor.movie.title,
      'character_type': actor.character_type
    } for actor in paginated_actors}
  })

@app.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movies(movie_id):
  try:
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie ID ' + str(movie_id) + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Movie ID ' + str(movie_id) + ' could not be deleted.')
  finally:
    db.session.close()

@app.route('/actors/<actor_id>', methods=['DELETE'])
def delete_actors(actor_id):
  try:
    actor = Actor.query.get(actor_id)
    db.session.delete(actor)
    db.session.commit()
    flash('Actor ID ' + str(actor_id) + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Actor ID ' + str(actor_id) + ' could not be deleted.')
  finally:
    db.session.close()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)