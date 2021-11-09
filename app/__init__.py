import os
import pickle5 as pickle
import numpy as np
import pandas as pd
import networkx as nx
from flask import Flask, Blueprint, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# DB - Sqlite3
dbsql = SQLAlchemy()
dbsql_path = 'sqlite:///db/betterpaths.db'
# Authentication
bcrypt = Bcrypt()
# Login
login_manager = LoginManager()

from .db.db_models import *

# Set up data for course searching, will be imported in courses module
cur_path = os.path.dirname(__file__)
with open(os.path.join(cur_path, 'resources/course_vectorizer.pickle'),'rb') as f:
    vectorizer = pickle.load(f)
with open(os.path.join(cur_path, 'resources/course_vectors.npz'),'rb') as f:
    course_vectors = pickle.load(f)
with open(os.path.join(cur_path, 'resources/graph.pickle'),'rb') as f:
    G = nx.read_gpickle(f)

df = pd.read_pickle(os.path.join(cur_path, 'resources/df_processed.pickle')).set_index('Code')

def create_app(config_class = Config):
    # Create app
    app = Flask(__name__)


    app.config.from_object(config_class)
    
    # sqlite db setup
    app.config['SQLALCHEMY_DATABASE_URI'] = dbsql_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    dbsql.init_app(app)
    with app.app_context():
        dbsql.create_all()
        dbsql.session.commit()
        # sanity check
        # from .db import db_general_testing.py
        from .db import resources_initializer

    bcrypt.init_app(app)
    

    from app.users.routes import users
    from app.courses.routes import courses
    app.register_blueprint(users)
    app.register_blueprint(courses)

    # Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    
    return app
