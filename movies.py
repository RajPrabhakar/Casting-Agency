from models import app, Movie, Character, Actor
from auth import requires_auth

from flask import jsonify, abort, request

## MOVIE ##

@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })
    except:
        abort(404)

@app.route('/movies/<id>', methods=['GET'])
@requires_auth('get:movie-detail')
def get_specific_movie(payload, id):
    try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        characters = Character.query.filter(Character.movie_id==id).all()
        cast = []
        for character in characters:
            actor_detail = None
            if not (character.actor_id is None):
                actor = Actor.query.filter(Actor.id==character.actor_id).one_or_none()
                actor_detail = {
                    'id': actor.id,
                    'name': actor.name,
                    'image': actor.image
                }
            character_detail = {
                'character_id': character.id,
                'character_name': character.name,
                'actor': actor_detail
            }
            cast.append(character_detail)
        movie_json = movie.format()
        movie_json['cast'] = cast
        return jsonify({
            'success': True,
            'movie': movie_json
        })
    except Exception as e:
        print(e)
        abort(404)

@app.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def post_movie(payload):
    body = request.get_json()
    if not ('title' in body and 'release_date' in body):
        abort(400)
    title = body.get('title')
    release_date = body.get('release_date')
    poster = body.get('poster')
    try:
        new_movie = Movie(title=title, release_date=release_date, poster=poster)
        new_movie.insert()
        return jsonify({
            'success': True,
            'movie': new_movie.format()
        })
    except:
        abort(422)

@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movie')
def patch_movie(payload, id):
    body = request.get_json()
    if not ('title' in body and 'release_date' in body):
        abort(400)
    title = body.get('title')
    release_date = body.get('release_date')
    poster = body.get('poster')
    try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        movie.title = title
        movie.release_date = release_date
        movie.poster = poster
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    except Exception as e:
        print(e)
        abort(422)

@app.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(payload, id):
    try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })
    except:
        abort(422)