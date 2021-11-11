import pytest
import json
from pathlib import Path
import os
from pytest_elasticsearch import fatories

from ..app import app, es
from ..app.searching_filtering.routes import search_home, performSearch

@pytest.fixture
def client():
    BASE_DIR =  Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    yield app.test_client()

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