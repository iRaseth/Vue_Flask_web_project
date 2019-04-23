import unittest
import env
from app import app, db
from app.database_models import User
from tests import BaseTestCase
from flask import json

"""This class tests login responses"""
class TestLogin(BaseTestCase):
    #Test if after successful login ure redirected to default page
    def test_login_success(self):
        response = self.client.post('/login',
            data = json.dumps(dict(username="test_user", password="test_password")),
            content_type = 'application/json'
        )
        self.assertIn('login success',response.data)
    #Test if after failed login you receive 'bad login'
    def test_login_failed(self):
        response = self.client.post('/login',
            data = json.dumps(dict(username='wrong_user', password='wrong_password')),
            content_type = 'application/json'
        )
        self.assertIn('wrong input data', response.data)
    #Test if fields are empty of half empty
    def test_login_failed_no_data(self):
        response = self.client.post('/login',
            data = json.dumps(dict(username='', password='')),
            content_type = 'application/json'
        )
        self.assertIn('wrong input data', response.data)
    #
    def test_login_failed_no_data_password(self):
        response = self.client.post('/login',
            data = json.dumps(dict(username='test_user', password='')),
            content_type = 'application/json'
        )
        self.assertIn('wrong input data', response.data)
    #
    def test_login_failed_no_data_login(self):
        response = self.client.post('/login',
            data = json.dumps(dict(username='', password='test_password')),
            content_type = 'application/json'
        )
        self.assertIn('wrong input data', response.data)


"""Tests routes that should be available only for users"""
class UsersRoutes(BaseTestCase):

    # Test if the response on successful logout is string 'uve been ...'
    def test_login_logout_success(self):
        self.client.post('/login',
            data = json.dumps(dict(username='test_user', password='test_password')),
            content_type = 'application/json'
        )
        response = self.client.get('/logout')
        self.assertIn('Uve been logged out', response.data)

    #Response of the failed logout should be unauthorized 401
    def test_logout_failed(self):
        response = self.client.get('/logout')
        self.assert401(response)

    #Test if the show_db returns 'fetched'
    def test_show_db_success(self):
        self.client.post('/login',
            data = json.dumps(dict(username='test_user', password='test_password')),
            content_type = 'application/json'
        )
        response_db_route = self.client.get('/show-db', content_type='html/text')
        self.assertIn('fetched',response_db_route.data)

    #Test if unauthorized request for showdb returns 401
    def test_show_db_failed(self):
        response = self.client.get('/show-db')
        self.assert401(response)

    #Test if the delete_users returns 'deleted'
    def test_delete_users_success(self):
        self.client.post('/login',
            data = json.dumps(dict(username='test_user', password='test_password')),
            content_type = 'application/json'
        )
        response_db_route = self.client.get('/delete-users', content_type='html/text')
        self.assertIn('deleted',response_db_route.data)

    #Test if unauthorized request for delete_users returns 401
    def test_delete_users_unauthorized(self):
        response = self.client.get('/delete-users', content_type='html/text')
        self.assert401(response)

    #Test if send_msg for authorized user returns 'u have added'
    def test_send_msg_success(self):
        self.client.post('/login',
            data = json.dumps(dict(username='test_user', password='test_password')),
            content_type = 'application/json'
        )
        response = self.client.post('/send_msg',
            data = json.dumps(dict(message='test_post')),
            content_type = 'application/json'
        )
        self.assertIn('u have added post', response.data)

    #Test if send_msg for unauthorized user returns 401
    def test_send_msg_failed(self):
        response = self.client.post('/send_msg',
            data = json.dumps(dict(message='test_post')),
            content_type = 'application/json'
        )
        self.assert401(response)

    #Test if authorized user sends get serv return err
    def test_send_msg_auth_failed(self):
        self.client.post('/login',
            data = json.dumps(dict(username='test_user', password='test_password')),
            content_type = 'application/json'
        )
        response = self.client.get('/send_msg',
            data = json.dumps(dict(message='test_post')),
            content_type = 'application/json'
        )
        self.assertIn('you cant send new message with GET method', response.data)

    #Test if user returns err when sending empty msg
    def test_send_msg_empty_failed(self):
        self.client.post('/login',
            data = json.dumps(dict(username='test_user', password='test_password')),
            content_type = 'application/json'
        )
        response = self.client.post('/send_msg',
            data = json.dumps(dict(message='')),
            content_type = 'application/json'
        )
        self.assertIn('u cant send empty msg', response.data)


if __name__ == '__main__':
    unittest.main()
