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

    # De-comment it if you need to test 2fa with CORECT OTP CODE
    # def test_signin_with_2fa(self):
    #     self.signup()
    #     response = self.client.post(
    #         url_for('twofa.twofa_setup'),
    #         data = {
    #             'name': self.username,
    #             'reset': False
    #         }
    #     )
    #     data = response.json['data']
    #     print(data)
    #     status = 400
    #     while status != 200:
    #         code = input('Enter otp code...')
    #         response = self.client.post(
    #             url_for('twofa.twofa_verify'),
    #             data = {
    #                 'name': self.username,
    #                 'code': code
    #             }
    #         )
    #         status = response.status_code
    #         if(status != 200):
    #             print(response.json['message'])

    #     response = self.client.post(
    #         url_for('signin.signin'),
    #         data={
    #             'name': self.username,
    #             'password': self.password
    #         }
    #     )
    #     assert response.status_code == 302

class Check2FA(SettingBase):
    def setup(self, name, reset):
        return self.client.post(
            url_for('twofa.twofa_setup'),
            data = {
                'name': name,
                'reset': reset
            }
        )

    def test_2fa_setup(self):
        self.signup_then_signin()
        response = self.setup(self.username, False)
        self.assert200(response)

        data = response.json['data']
        assert 'totp_secret' in data
        assert 'qrcode' in data

    def test_2fa_NoUser(self):
        response = self.setup(self.username, False)
        self.assert400(response)

    def test_2fa_reset(self):
        self.signup_then_signin()
        response = self.setup(self.username, False)
        secret_key = response.json['data']['totp_secret']
        response = self.setup(self.username, True)
        self.assert200(response)
        assert secret_key != response.json['data']['totp_secret']

    # De-comment it if you need to test 2fa with CORECT OTP CODE
    # def test_2fa_verify_CorectCode(self):
    #     self.signup_then_signin()
    #     response = self.setup(self.username, False)
    #     data = response.json['data']
    #     print(data)
    #     code = input('Enter otp code...')
    #     response = self.client.post(
    #         url_for('twofa.twofa_verify'),
    #         data = {
    #             'name': self.username,
    #             'code': code
    #         }
    #     )
    #     self.assert200(response)

    def test_2fa_verify_ErrorCode(self):
        self.signup_then_signin()
        self.setup(self.username, False)
        response = self.client.post(
            url_for('twofa.twofa_verify'),
            data = {
                'name': self.username,
                'code': '000000'
            }
        )
        self.assert400(response)

if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(CheckSignin('test_signin'))
    suite.addTest(CheckSignup('test_signup'))
    suite.addTest(Check2FA('test_2fa'))

    unittest.main()