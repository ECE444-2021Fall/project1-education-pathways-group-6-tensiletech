import pytest
import json
from pathlib import Path
from sqlalchemy import insert

from ..app import dbsql, dbsql_path
from ..app.db.db_models import User, CourseComments, Courses, CourseComments

# Test added by Anikeith Bankar
@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    app.config["DATABASE"] = BASE_DIR.joinpath("../db/betterpaths.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbsql_path}"

    dbsql.create_all()  # setup
    yield app.test_client()  # tests run here
    dbsql.drop_all()  # teardown

def test_database(client):
    """initial test. ensure that the database exists"""
    at_location = Path("betterpaths.db").is_file()
    assert at_location

def insert_user(client):
    stmt = (
        insert(User).
        values(id=1, username='Keith Bankar', email='anikeith@yahoo.com', password='bankar')
    )
    assert stmt
