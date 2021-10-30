import unittest
import os
from flask import current_app
from app import create_app, db

app = create_app()

class BasicsTestCase(unittest.TestCase):
    ############  SET UP  ############
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    ########  HELPER METHODS  ########
    def login(self, username, password):
        return self.app.post(
            "/login",
            data=dict(username=username, password=password),
            follow_redirects=True
        )
    
    ############   TESTS   ###########
    def test_search_redirection(self): # test function written by Hannah (comments for lab6 propose)
        self.login(app.config["USERNAME"], app.config["PASSWORD"])
        rv = self.app.get("/search/?query=test", follow_redirects=True) # there should be pre-existing course information that contains 'test' in the test db
        self.assertIn(b'This is the test data that should be search for', rv.data) #test course description
        self.assertIn(b'&lt;TEST101&gt;', rv.data) # This should be the course code for the test course 'TEST101'