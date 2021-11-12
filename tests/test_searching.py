import pytest
import json
from pathlib import Path
import os
from pytest_elasticsearch import factories
from flask import url_for, request
from urllib.parse import urlparse

from app import create_app, es
from app.searching_filtering.routes import search_home, performSearch

app = create_app()

############  SET UP  ############
@pytest.fixture
def client():
    BASE_DIR =  Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    yield app.test_client()

########  HELPER METHODS  ########
def login(client, username, password):
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )
############   TESTS   ###########
def test_redir_login(client):
    response = client.get("/", content_type="html/text", follow_redirects=False)
    expectedPath = '/login'
    assert response.status_code == 302
    assert urlparse(response.location).path == expectedPath
