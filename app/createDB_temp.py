# Delete file later
# Running this file once may help the database if not created already

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# If the statement below doesnt work to help in creating user class, uncomment the code on line 14
from models import User as User
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True) # Generated automatically when not specified
#     username = db.Column(db.String(100), unique = True, nullable = False)
#     email = db.Column(db.String(100), unique = True, nullable = False)
#     password = db.Column(db.String(100), nullable = False)

db.create_all()
db.session.commit()


