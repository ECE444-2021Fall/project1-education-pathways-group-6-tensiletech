import unittest

from app import create_app
from app.models import User

class UsersTest(unittest.TestCase): # this test was written by Justin (lab6)
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_create_page(self):
        response = self.client.get('/signup')
        self.assertTrue(response.status_code, 200)
        self.assertTrue('Sign Up' in response.get_data(as_text=True))

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertTrue(response.status_code, 200)
        self.assertTrue('Welcome Back' in response.get_data(as_text=True))

    def test_invalid_login(self):
        response = self.client.post('/login', data={
            'username': 'invalidUsername',
            'password': 'invalidPassword'
        })
        self.assertTrue(response.status_code, 200)
        self.assertTrue('Incorrect username or password' in response.get_data(as_text=True))
