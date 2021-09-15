from logging import error
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from models import setup_db, Movie, Actor, Character
from auth import AuthError, requires_auth

app = Flask(__name__)

app.config.from_object('config')

setup_db(app)

CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

## INDEX ##

@app.route('/')
def index():
    return jsonify({
        'success': True,
        'available_links': {
            'movies': '/movies',
            'actors': '/actors',
            'character': '/character'
        },
        'access_tokens': {
            'casting_assistant': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5aRjd1Nlg3UHRDQWpBWkNjQVFaTiJ9.eyJpc3MiOiJodHRwczovL3Jhai0xODA0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNzQ5NzI5MDUzNjk3OTg2NzMxOSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjMxNjk4MTgxLCJleHAiOjE2MzE3MDUzODEsImF6cCI6Im1mcVpTR1k1WDAwMGVxWnVVSFdHNXRNUkZOVmRPdTByIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3ItZGV0YWlsIiwiZ2V0OmNoYXJhY3Rlci1kZXRhaWwiLCJnZXQ6bW92aWUtZGV0YWlsIl19.DYc0JvNr5lX1_P4FxWDKNz5GRUdLXgtINxhNVLZUdRnPUDHu_fGwZ8Gk5zRCfO1rzfNe_Dhwqdm_zhwoex-U4kYd_zPIyMOybiNkQsqjwu1Qp1l9HlCdnJ-9T_prBjMjpN3IUl1bgI2FmzWgL6cFVUMXmOUBLIxyX5bOjJmUHObyMsFOKBFhLJUfBPy1QIrasYlkOJfIy9ch5oC_5Y76jbK6F-_85whMeKjuqMAYK-z9oTCwUxFHIDWKs_dvY4PrS_tg4Th6JCOMC1caX6btju7enmda0m5LkXL0uK6YrdP8qax2hMdiQzI8QUJ5cg8P9OjnzbN0hfTc4v6-iBXnzw',
            'casting_director': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5aRjd1Nlg3UHRDQWpBWkNjQVFaTiJ9.eyJpc3MiOiJodHRwczovL3Jhai0xODA0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMDc4ODc2MDY2MzYxMTc0NjYzMCIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjMxNjk5MTU3LCJleHAiOjE2MzE3MDYzNTcsImF6cCI6Im1mcVpTR1k1WDAwMGVxWnVVSFdHNXRNUkZOVmRPdTByIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6Y2hhcmFjdGVyIiwiZ2V0OmFjdG9yLWRldGFpbCIsImdldDpjaGFyYWN0ZXItZGV0YWlsIiwiZ2V0Om1vdmllLWRldGFpbCIsInBhdGNoOmFjdG9yIiwicGF0Y2g6Y2hhcmFjdGVyIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDpjaGFyYWN0ZXIiXX0.ZT84YbDGX9VN81_Mo6_OTchw0JLgGMhAkYLmM6USHVBIeDYNZ5Fb4-C1q9blmNUgbw6OmHpbExPFDxlghSMVjcVEHbnppDboBaPAO_3c9dRi4KC7sUBTUTjmrf-nakzAwdQVBkkkMvMII0oRxHNHtILj6TIbiRxSt7bld1Trbo2wkmsSnvS5_eeR3lVxwtXQPLIdB-WlkisEphgRL_gWktUSyfRq7FBjzJv-jO7wRmZcGjXBpSO-kQsFyzs8ybI2L0bsvai4qtuGGeB-bJzvVFgHcrFmcYZQodfuK9GZr8nLkSe8sgnbzCTEc8fGDSK0wg3RXsIOVFiG0G6YMUNaeA',
            'executive_producer': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5aRjd1Nlg3UHRDQWpBWkNjQVFaTiJ9.eyJpc3MiOiJodHRwczovL3Jhai0xODA0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjMwOTg0MTM2Mjg3OTY0MjExNyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjMxNjk5NjA3LCJleHAiOjE2MzE3MDY4MDcsImF6cCI6Im1mcVpTR1k1WDAwMGVxWnVVSFdHNXRNUkZOVmRPdTByIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6Y2hhcmFjdGVyIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yLWRldGFpbCIsImdldDpjaGFyYWN0ZXItZGV0YWlsIiwiZ2V0Om1vdmllLWRldGFpbCIsInBhdGNoOmFjdG9yIiwicGF0Y2g6Y2hhcmFjdGVyIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDpjaGFyYWN0ZXIiLCJwb3N0Om1vdmllIl19.IPqarl08kTHwMoq3O7RoKvFo6n6zIbk_42dtpnH-VF0Y3uwTOh__LffxKq5u4pS_TXEKlvwSu1N3lqGoE6Qim_0o2Gcg3h6MYH83nzndLivw0R9QN2sBc9U6d06QDx6TAbaTkp-hTYBPIqjeq9NTS96DZIsDxPtiVIGUHDavhKtOtW7MPQMDm4eKrSS2YBDFfLmpYE0SWVyrh_UF-I9o_qRYKq7IjX3-i-6GYC8w07qrTbD6-FDGmJ6E3GgszmzQgpeofUOO_O_zY5hqycux7opg1uz1ECGz_w5VCFKo1nl-AiUz-Cjw37c7v1EYnWxhMC1mQ_GfTXIYxVmgDuJDBw'
        }
    })

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
        if movie is None:
            abort(404)
        movie_json = movie.format()
        movie_json['cast'] = cast
        return jsonify({
            'success': True,
            'movie': movie_json
        })
    except:
        abort(422)

@app.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def post_movie(payload):
    body = request.get_json()
    if not ('title' in body and 'release_date' in body):
        abort(422)
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
    except error as e:
        print(e)
        abort(422)

@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movie')
def patch_movie(payload, id):
    body = request.get_json()
    if not ('title' in body and 'release_date' in body):
        abort(422)
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
    except error as e:
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
        abort(422)
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
    except error as e:
        print(e)
        abort(422)

@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actor')
def patch_actor(payload, id):
    body = request.get_json()
    if not ('name' in body and 'age' in body and 'gender' in body):
        abort(422)
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
    except error as e:
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
        if character is None:
            abort(404)
        return jsonify({
            'success': True,
            'character': character.format()
        })
    except:
        abort(404)

@app.route('/characters', methods=['POST'])
@requires_auth('post:character')
def post_character(payload):
    body = request.get_json()
    if not ('name' in body and 'movie_id' in body and 'actor_id' in body):
        abort(422)
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
    except error as e:
        print(e)
        abort(422)

@app.route('/characters/<id>', methods=['PATCH'])
@requires_auth('patch:character')
def patch_character(payload, id):
    body = request.get_json()
    if not ('name' in body and 'movie_id' in body and 'actor_id' in body):
        abort(422)
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
    except error as e:
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code

if __name__ == '__main__':
    app.run()