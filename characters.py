from models import app, Movie, Character, Actor
from auth import requires_auth

from flask import jsonify, abort, request

## CHARACTER ##

@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        characters = Character.query.all()
        return jsonify({
            'success': True,
            'characters': [character.format() for character in characters]
        })
    except:
        abort(404)

@app.route('/characters/<id>', methods=['GET'])
@requires_auth('get:character-detail')
def get_specific_character(payload, id):
    try:
        character = Character.query.filter(Character.id == id).one_or_none()
        movie = Movie.query.filter(Movie.id==character.movie_id).one_or_none()
        actor = Actor.query.filter(Actor.id==character.actor_id).one_or_none()
        character_json = character.format()
        character_json['movie_title'] = movie.title
        character_json['actor_name'] = actor.name
        if character is None:
            abort(404)
        return jsonify({
            'success': True,
            'character': character_json
        })
    except:
        abort(404)

@app.route('/characters', methods=['POST'])
@requires_auth('post:character')
def post_character(payload):
    body = request.get_json()
    if not ('name' in body and 'movie_id' in body):
        abort(400)
    name = body.get('name')
    movie_id = body.get('movie_id')
    actor_id = body.get('actor_id')
    try:
        new_character = Character(name=name, movie_id=movie_id, actor_id=actor_id)
        new_character.insert()
        return jsonify({
            'success': True,
            'character': new_character.format()
        })
    except Exception as e:
        print(e)
        abort(422)

@app.route('/characters/<id>', methods=['PATCH'])
@requires_auth('patch:character')
def patch_character(payload, id):
    body = request.get_json()
    if not ('name' in body and 'movie_id' in body):
        abort(400)
    name = body.get('name')
    movie_id = body.get('movie_id')
    actor_id = body.get('actor_id')
    try:
        character = Character.query.filter(Character.id == id).one_or_none()
        if character is None:
            abort(404)
        character.name = name
        character.movie_id = movie_id
        character.actor_id = actor_id
        character.update()
        return jsonify({
            'success': True,
            'character': character.format()
        })
    except Exception as e:
        print(e)
        abort(422)

@app.route('/characters/<id>', methods=['DELETE'])
@requires_auth('delete:character')
def delete_character(payload, id):
    try:
        character = Character.query.filter(Character.id == id).one_or_none()
        if character is None:
            abort(404)
        character.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })
    except:
        abort(422)