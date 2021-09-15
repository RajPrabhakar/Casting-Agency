import os, unittest, json
from dotenv import load_dotenv

from app import setup_db, create_app

load_dotenv()

CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT')
CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR')
EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER')

class CastingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')
        setup_db(self.app, self.database_path)

    def tearDown(self):
        pass

    ## SUCCESS BEHAVIOUR ##
    # MOVIE
    def get_movie_200(self):
        res = self.client().get(
            '/movies/1',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def post_movie_200(self):
        res = self.client().post(
            '/movies',
            json={
                "title": "The Hobbit: The Desolation of Smaug",
                "release_date": "12/13/2013",
                "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def patch_movie_200(self):
        res = self.client().post(
            '/movies/1',
            json={
                "title": "The Hobbit 2: The Desolation of Smaug",
                "release_date": "12/13/2013",
                "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def delete_movie_200(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])

    # ACTOR
    def get_actor_200(self):
        res = self.client().get(
            '/actors/1',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def post_actor_200(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "Benedict Cumberbatch",
                "age": "45",
                "gender": "male",
                "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def patch_actor_200(self):
        res = self.client().post(
            '/actors/1',
            json={
                "name": "Mr. Benedict Cumberbatch",
                "age": "45",
                "gender": "male",
                "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def delete_actor_200(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])

    # CHARACTER
    def get_character_200(self):
        res = self.client().get(
            '/characters/1',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['character'])

    def post_character_200(self):
        res = self.client().post(
            '/characters',
            json={
                "name": "Bilbo Baggins",
                "movie_id": "1",
                "actor_id": "1"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['character'])

    def patch_character_200(self):
        res = self.client().post(
            '/characters/1',
            json={
                "name": "Bilbo Baggins",
                "movie_id": "2",
                "actor_id": "2"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['character'])

    def delete_character_200(self):
        res = self.client().delete(
            '/characters/1',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])

    ## FAILURE BEHAVIOUR ##
    # MOVIE
    def get_movie_404(self):
        res = self.client().get(
            '/movies/100',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['error'])

    def post_movie_400(self):
        res = self.client().post(
            '/movies',
            json={
                "release_date": "12/13/2013",
                "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def patch_movie_400(self):
        res = self.client().post(
            '/movies/1',
            json={
                "release_date": "12/13/2013",
                "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def delete_movie_404(self):
        res = self.client().delete(
            '/movies/100',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['error'])

    # ACTOR
    def get_actor_404(self):
        res = self.client().get(
            '/actors/100',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['error'])

    def post_actor_400(self):
        res = self.client().post(
            '/actors',
            json={
                "age": "45",
                "gender": "male",
                "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def patch_actor_400(self):
        res = self.client().post(
            '/actors/1',
            json={
                "age": "45",
                "gender": "male",
                "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def delete_actor_405(self):
        res = self.client().delete(
            '/actors',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertTrue(data['error'])

    # CHARACTER
    def get_character_404(self):
        res = self.client().get(
            '/characters/100',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['error'])

    def post_character_400(self):
        res = self.client().post(
            '/characters',
            json={
                "movie_id": "1",
                "actor_id": "1"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def patch_character_400(self):
        res = self.client().post(
            '/characters/1',
            json={
                "movie_id": "2",
                "actor_id": "2"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def delete_character_405(self):
        res = self.client().delete(
            '/characters',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertTrue(data['error'])

    ## RBAC Tests ##
    # EXECUTIVE PRODUCER
    def test_post_movie_EP_200(self):
        res = self.client().post(
            '/movies',
            json={
                "title": "The Hobbit: The Desolation of Smaug",
                "release_date": "12/13/2013",
                "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def test_post_actor_EP_200(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "Benedict Cumberbatch",
                "age": "45",
                "gender": "male",
                "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
            },
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def test_get_movie_EP_200(self):
        res = self.client().get(
            '/movies/1',
            headers={
                "Authorization": "Bearer " + EXECUTIVE_PRODUCER
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    # CASTING DIRECTOR
    def test_post_movie_CD_403(self):
        res = self.client().post(
            '/movies',
            json={
                "title": "The Hobbit: The Desolation of Smaug",
                "release_date": "12/13/2013",
                "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg"
            },
            headers={
                "Authorization": "Bearer " + CASTING_DIRECTOR
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['error'])

    def test_post_actor_CD_200(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "Benedict Cumberbatch",
                "age": "45",
                "gender": "male",
                "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
            },
            headers={
                "Authorization": "Bearer " + CASTING_DIRECTOR
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def test_get_movie_CD_200(self):
        res = self.client().get(
            '/movies/1',
            headers={
                "Authorization": "Bearer " + CASTING_DIRECTOR
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    # CASTING ASSISTANT
    def test_post_movie_CA_403(self):
        res = self.client().post(
            '/movies',
            json={
                "title": "The Hobbit: The Desolation of Smaug",
                "release_date": "12/13/2013",
                "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg"
            },
            headers={
                "Authorization": "Bearer " + CASTING_ASSISTANT
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['error'])

    def test_post_actor_CA_403(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "Benedict Cumberbatch",
                "age": "45",
                "gender": "male",
                "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
            },
            headers={
                "Authorization": "Bearer " + CASTING_ASSISTANT
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['error'])

    def test_get_movie_CA_200(self):
        res = self.client().get(
            '/movies/1',
            headers={
                "Authorization": "Bearer " + CASTING_ASSISTANT
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

if __name__ == "__main__":
    unittest.main()