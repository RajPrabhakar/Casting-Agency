from models import app, Movie, Character, Actor
from auth import requires_auth

from flask import jsonify, abort, request

## ACTOR ##

@app.route('/actors', methods=['GET'])
def get_actors():
    try:
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })
    except:
        abort(404)

@app.route('/actors/<id>', methods=['GET'])
@requires_auth('get:actor-detail')
def get_specific_actor(payload, id):
    try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        characters = Character.query.join(Movie).filter(Character.actor_id==id).all()
        movies = []
        for character in characters:
            character_detail = {
                'character_id': character.id,
                'character_name': character.name,
                'movie': {
                    'id': character.movie_id,
                    'title': character.movie.title,
                    'poster': character.movie.poster
                }
            }
            movies.append(character_detail)
        if actor is None:
            abort(404)
        actor_json = actor.format()
        actor_json['movies'] = movies
        return jsonify({
            'success': True,
            'actor': actor_json
        })
    except:
        abort(404)

@app.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def post_actor(payload):
    body = request.get_json()
    if not ('name' in body and 'age' in body and 'gender' in body):
        abort(400)
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    image = body.get('image')
    try:
        new_actor = Actor(name=name, age=age, gender=gender, image=image)
        new_actor.insert()
        return jsonify({
            'success': True,
            'actor': new_actor.format()
        })
    except Exception as e:
        print(e)
        abort(422)

@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actor')
def patch_actor(payload, id):
    body = request.get_json()
    if not ('name' in body and 'age' in body and 'gender' in body):
        abort(400)
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    image = body.get('image')
    try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.image = image
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    except Exception as e:
        print(e)
        abort(422)

@app.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(payload, id):
    try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })
    except:
        abort(422)