from app import dbsql
from flask_login import UserMixin # Helps in managing a user session

class ExampleTable(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)

class User(dbsql.Model, UserMixin):
    id = dbsql.Column(dbsql.Integer, primary_key = True) # Generated automatically when not specified
    username = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    email = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    password = dbsql.Column(dbsql.String(100), nullable = False)
