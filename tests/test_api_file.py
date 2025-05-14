import unittest
from flask import url_for, Response
from flask_testing import TestCase
from api import create_app
import random, string

class SettingBase(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.username = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        self.password = 'admin'

    def tearDown(self):
        pass

    def signup(self) -> Response:
        response = self.client.post(
            url_for('signup.signup'),
            data={
                'name': self.username,
                'password': self.password
            }
        )
        return response
    
    def signup_then_signin(self) -> Response:
        self.client.post(
            url_for('signup.signup'),
            data={
                'name': self.username,
                'password': self.password
            }
        )
        response = self.client.post(
            url_for('signin.signin'),
            data={
                'name': self.username,
                'password': self.password
            }
        )
        return response

class CheckUpload(SettingBase):
    def test_upload(self):
        response = self.signup_then_signin()
        token = response.json['data']['access_token']
        print(token)
        response = self.client.post(
            url_for('upload.upload'),
            data = {
                'name': self.username,
                'access_token': token
            }
        )
        self.assert200(response)

        
if __name__ == '__main__':
    unittest.TestSuite()
    unittest.main()