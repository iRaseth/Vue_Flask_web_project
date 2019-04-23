import unittest
import env
from app import app, db
from app.database_models import User
from flask_testing import TestCase
from flask import json

"""A base test case."""
class BaseTestCase(TestCase):
    
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        #db.session.add(BlogPost("Test post", "This is a test. Only a test."))
        test_user = User(username='test_user')
        test_user.set_password('test_password')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

"""This class tests the proper app responses."""
class FlaskHTTPTester(BaseTestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        response_index = self.client.get('/index', content_type='html/text')
        self.assert200(response)
        self.assert200(response_index)

    # Test the register route with GET method
    def test_register_get(self):
        response = self.client.get('/register')
        self.assert405(response)

    # Test the register route with POST method
    def test_register_post(self):
        response = self.client.post('/register',
            data = json.dumps(dict(username = "", password="")),
            content_type = 'application/json'
        )
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()
