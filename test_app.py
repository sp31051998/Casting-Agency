import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Movie, Actor


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "CastingAgency"
        self.database_path = "postgres://postgres:shubham@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Amir Khan',
            'age': '50',
            'gender' : 'Male'
        }
        self.new_movie = {
            'title' : '3 Idiots',
            'release_date' : '2020-05-06'
        }
        self.update_actor = {
            'age' : '45'
        }
        self.update_movie = {
            'title' : 'Life of a Pie'
        }

        
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        pass
    
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])
    
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    #TO do POST withourt permission

    def test_update_actor(self):
        res = self.client().patch('/actors/62', json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
    
    def test_update_actor_with_incorrect_id(self):
        res = self.client().patch('/actors/20000', json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_delete_actor(self):
        id = 64
        res = self.client().delete('/actors/' + str(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)

    def test_delete_actor_incorrect_id(self):
        id = 2000
        res = self.client().delete('/actors/' + str(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])
    
    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    # #TO do POST request with no permission

    def test_update_movie(self):
        res = self.client().patch('/movies/20', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
    
    def test_update_movie_with_incorrect_id(self):
        res = self.client().patch('/movies/20000', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_delete_movie(self):
        id = 20  
        res = self.client().delete('/movies/' + str(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)

    def test_delete_movie_incorrect_id(self):
        id = 2000
        res = self.client().delete('/movies/' + str(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    
    
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

