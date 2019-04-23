import unittest
import env
from app import app, db
from app.database_models import User
from tests import BaseTestCase
from flask import json

class TestRegistration(BaseTestCase):
    """
    Test the registration feature
    """

    #User doesnt exist in database
    def test_register_success(self):
        response = self.client.post('/register',
            data = json.dumps(dict(username="test_user_new", password="test_password_new")),
            content_type = 'application/json'
        )
        self.assertIn('user has been created successfuly',response.data)
    #User already exist in database
    def test_register_failed_user_exist(self):
        response = self.client.post('/register',
            data = json.dumps(dict(username="test_user", password="test_password")),
            content_type = 'application/json'
        )
        self.assertIn('user with this nickname already exist',response.data)
    #Empty fields were send
    def test_register_failed_no_data(self):
        response = self.client.post('/register',
            data = json.dumps(dict(username='', password='')),
            content_type = 'application/json'
        )
        self.assertIn('please input login and password for registration',response.data)

    def test_register_failed_password_no_data(self):
        response = self.client.post('/register',
            data = json.dumps(dict(username="test_user", password="")),
            content_type = 'application/json'
            )
        self.assertIn('please input login and password for registration',response.data)

    def test_register_failed_user_no_data(self):
        response = self.client.post('/register',
            data = json.dumps(dict(username="", password="test_user")),
            content_type = 'application/json'
            )
        self.assertIn('please input login and password for registration',response.data)

if __name__ == '__main__':
    unittest.main()
