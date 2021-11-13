import pytest
import json
from pathlib import Path
import os
from flask import url_for, request
from urllib.parse import urlparse
from flask_wtf.csrf import CSRFError, CSRFProtect

from app import create_app, es, dbsql, dbsql_path
from app.searching_filtering.routes import search_home, performSearch, get_data
from app.db.db_models import User, add_to_table

app = create_app()

#Test username and password
USERNAME = 'admin'
PASSWORD = 'admin'
SEARCH_RESULT_SIZE = 5

############  SET UP  ############
@pytest.fixture
def client():
    BASE_DIR =  Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        dbsql.create_all()
        dbsql.session.commit()
    yield app.test_client()
    with app.app_context():
        dbsql.drop_all()

########  HELPER METHODS  ########
def login(client, username, password):
    client.post(
        "/signup",
        data=dict(email="123@g.com", username=username, password=password, confirm_password=password, submit=True),
        follow_redirects=True
    )
    return client.post(
        "/login",
        data=dict(username=username, password=password, submit=True),
        follow_redirects=True
    )

def logout(client):
    client.post("/logout", follow_redirects=True)
############   TESTS   ###########
def test_redir_to_login(client):
    '''Test the redirection to login page if user not logged in'''
    response = client.get("/", content_type="html/text", follow_redirects=False)
    expectedPath = '/login'
    assert response.status_code == 302
    assert urlparse(response.location).path == expectedPath

def test_search_home_logged_in(client):
    '''Test the search page status code when user in logged in'''
    login(client, USERNAME, PASSWORD)
    response = client.get("/", content_type="html/text", follow_redirects=False)
    assert response.status_code != 302 # not getting redirected
    assert response.status_code == 200 # OK
    assert b"<h3>Welcome to BetterPath!</h3>" in response.data # home page title

def test_search_result_redirection(client):
    '''Test searching result page redirection'''
    login(client, USERNAME, PASSWORD)
    rv = client.post("/", data=dict(keywords='', search=True, select='Any', divisions='Any', campuses='Any'))
    assert b"<h1>Search Results</h1>" in rv.data

def test_search_with_incorrect_keyword(client):
    '''Test the search result with incorrect keyword'''
    login(client, USERNAME, PASSWORD)
    rv = client.post("/", data=dict(keywords='sdfghj', search=True, select='Any', divisions='Any', campuses='Any'))
    assert b'Sorry, There are No Courses Matching Your Search!' in rv.data

def test_get_data_blank_keyword():
    '''Test the get_data function when no search term applied and with default filters'''
    output = get_data("__", 'Any', 'Any', 'Any', SEARCH_RESULT_SIZE)
    output_list = []
    for i in output['hits']['hits']:
        output_list.append(i['_source']['Code'])
    expected = ['ENGB29H3', 'JMU421H1', 'PSY220H5', 'ARC382H1', 'ACMC01H3']
    assert output_list == expected

def test_get_data_with_correct_keyword():
    '''Test the get_data function when correct search term applied with default filters'''
    output = get_data("software", 'Any', 'Any', 'Any', SEARCH_RESULT_SIZE)
    output_list = []
    for i in output['hits']['hits']:
        output_list.append(i['_source']['Code'])
    expected = ['ECE444H1', 'CSC207H5', 'CSC207H1', 'CSCB07H3', 'ECE353H1']
    assert output_list == expected

def test_get_data_fuzziness():
    '''Test get_data when there is a slight typo in the search term'''
    output = get_data("stfoware", 'Any', 'Any', 'Any', SEARCH_RESULT_SIZE)
    output_list = []
    for i in output['hits']['hits']:
        output_list.append(i['_source']['Code'])
    expected = ['ECE444H1', 'CSC207H5', 'CSC207H1', 'CSCB07H3', 'ECE353H1']
    assert output_list == expected

    output = get_data("stfoware", 'Any', 'Any', 'Any', SEARCH_RESULT_SIZE)
    output_list = []
    for i in output['hits']['hits']:
        output_list.append(i['_source']['Code'])
    expected = ['ECE444H1', 'CSC207H5', 'CSC207H1', 'CSCB07H3', 'ECE353H1']
    assert output_list == expected

def test_get_data_filter_with_no_keywords():
    '''Test the get_data with filters applied but no search term input'''
    output = get_data("__", '4', 'Faculty of Applied Science & Engineering', 'Any', SEARCH_RESULT_SIZE)
    output_list = []
    for i in output['hits']['hits']:
        output_list.append(i['_source']['Code'])
    expected = ['MIE498Y1', 'MSE492H1', 'MSE461H1', 'CHE430Y1', 'MIN466H1']
    assert output_list == expected
    
