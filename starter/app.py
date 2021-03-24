import os
import json

from flask import Flask, request, abort, jsonify, flash, render_template
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
  
  return render_template('/movies')

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

  return render_template('/actors')

@app.route('/movies', methods=['POST'])
def post_movie():
  request_body = request.get_json()
  movie_id = request_body.get('id')
  movie_title = request.get('title')
  movie_year = request.get('year')
  movie_director = request.get('director')
  if movie_id is None or movie_title is None or movie_year is None or movie_director is None:
    abort(422)
  
  try:
    movie = Movie(id=movie_id,
                  title=movie_title,
                  year=movie_year,
                  director=movie_director)
    db.session.add(movie)
    db.session.commit()
    flash('Movie ' + str(movie_title) + ' was successfully added!')
  except:
    db.session.rollback()
    flask('An error occurred. Movie ' + str(movie_title) + ' could not be added!')
  finally:
    db.session.close()

  return render_template('/movies')

@app.route('/actors', methods=['POST'])
def post_actor():
  request_body = request.get_json()
  movie_id = request_body.get('film_id')
  actor_name = request_body.get('name')
  actor_character_type = request_body.get('character_type')
  if actor_id is None or film_id is None or actor_name is None or actor_character_type is None:
    abort(422)
  
  try:
    actor = Actor(film_id=movie_id,
                  name=actor_name,
                  character_type=actor_character_type)
    db.session.add(actor)
    db.session.commit()
    flash('Actor ' + str(actor_name) + ' was successfully added!')
  except:
    db.session.rollback()
    flask('An error occurred. Actor ' + str(actor_name) + 'could not be added!')
  finally:
    db.session.close()
  
  return render_template('/actors')

@app.route('/movies/<movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
  request_body = request.get_json()
  movie_title = request_body.get('title')
  movie_year = request_body.get('year')
  movie_director = request_body.get('director')
  if movie_title is None or movie_year is None or movie_director is None:
    abort(422)
  
  try:
    movie = Movie.query.get(movie_id)
    if movie_title is not None:
      movie.title = movie_title
    elif movie_year is not None:
      movie.year = movie_year
    elif movie_director is not None:
      movie.director = movie_director
    db.session.commit()
    flash('Movie ' + movie_id + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Movie ' + movie_id + ' could not be updated!')
  finally:
    db.session.close()
  
  return render_template('/movies')

@app.route('/actors/<actor_id>', methods=['PATCH'])
def patch_actor(actor_id):
  request_body = request.get_json()
  movie_id = request_body.get('film_id')
  actor_name = request_body.get('name')
  actor_character_type = request_body.get('character_type')
  if movie_id is None or actor_name is None or actor_character_type is None:
    abort(422)
  
  try:
    actor = Actor.query.get(actor_id)
    if movie_id is not None:
      actor.film_id = movie_id
    elif actor_name is not None:
      actor.name = actor_name
    elif actor_character_type is not None:
      actor.character_type = actor_character_type
    db.session.commit()
    flash('Actor ' + actor_id + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Actor ' + actor_id + ' could not be updated!')
  finally:
    db.session.close()
  
  return render_template('/actors')

@app.errorhandler(400)
def bad_request_error(error):
  return jsonify({
    'success': False,
    'error': '400',
    'message': 'Bad Request'
  }), 400

@app.errorhandler(404)
def not_found_error(error):
  return jsonify({
    'success': False,
    'error': '404',
    'message': 'Not Found'
  }), 404

@app.errorhandler(405)
def not_allowed_error(error):
  return jsonify({
    'success': False,
    'error': '405',
    'message': 'Method Not Allowed'
  }), 405

@app.errorhandler(422)
def unprocessable_error(error):
  return jsonify({
    'success': False,
    'error': '422',
    'message': 'Unprocessable'
  }), 422

@app.errorhandler(500)
def server_error(error):
  return jsonify({
    'success': False,
    'error': '500',
    'message': 'Internal Server Error'
  }), 500

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)