import unittest
from flask import url_for, Response
from flask_testing import TestCase
from api import create_app

class SettingBase(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.username = 'test001'
        self.password = 'admin'

    def tearDown(self):
        from database import get_db
        get_db()._clean()
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
    
class CheckSignup(SettingBase):
    def test_signup(self):
        response = self.signup()
        self.assert200(response)
        data = response.json['data']
        assert data['name'] == self.username
        assert data['totp_secret'] == None
    
    def test_multi_signup(self):
        response = self.signup()
        response = self.signup()
        self.assert_403(response)

class CheckSignin(SettingBase):
    def test_success_signin(self):
        self.signup()
        response = self.client.post(
            url_for('signin.signin'),
            data={
                'name': self.username,
                'password': self.password
            }
        )
        self.assert200(response)

        data = response.json['data']
        keys = data.keys()
        assert 'name' in keys
        assert 'totp_secret' in keys
        assert 'access_token' in keys
    
    def test_nonexist_user(self):
        self.signup()
        response = self.client.post(
            url_for('signin.signin'),
            data={
                'name': 'hahaha',
                'password': self.password
            }
        )
        self.assert400(response)

    def test_error_password(self):
        self.signup()
        response = self.client.post(
            url_for('signin.signin'),
            data={
                'name': self.username,
                'password': 'hahaha'
            }
        )
        self.assert401(response)

if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(CheckSignin('test_signin'))
    suite.addTest(CheckSignup('test_signup'))

    unittest.main()