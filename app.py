import os
from dotenv import load_dotenv
from flask import jsonify, Flask, abort, request
from flask_cors import CORS

from models import Movie, Actor, Character, setup_db
from auth import requires_auth, AuthError
import config

load_dotenv()

def create_app(database_name):
    app = Flask(__name__)
    app.config.from_object('config')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_name

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
                'casting_assistant': config.CASTING_ASSISTANT,
                'casting_director': config.CASTING_DIRECTOR,
                'executive_producer': config.EXECUTIVE_PRODUCER
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

    ## ERROR HANDLER ##

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "invalid syntax"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

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

    return app

app = create_app(os.getenv('SQLALCHEMY_DATABASE_URI'))

if __name__ == '__main__':
    app.run()