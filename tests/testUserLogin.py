import pytest
import os
from pathlib import Path
from app import app


@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True

    yield app.test_client() # tests run here

def loginTest(client): # Test written by Romil Jain for Lab 6
    rv = client.post("/login", data=dict(username="romil8", password="romil"),
        follow_redirects=True)
    if b"Already logged in!" in rv.data or b"Successfully logged in!" in rv.data:
        assert True
    else:
        assert False

    