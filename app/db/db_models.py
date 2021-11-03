from app import dbsql
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin # Helps in managing a user session

Base = declarative_base()
class User(Base, UserMixin):
    __tablename__ = 'user'
    id = dbsql.Column(dbsql.Integer, primary_key = True) # Generated automatically when not specified
    username = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    email = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    password = dbsql.Column(dbsql.String(100), nullable = False)

    def __repr__(self):
        return f"User(UserId: '{self.id}', Username: '{self.username}', email: '{self.email}')"
class Courses(Base):
    __tablename__ = 'courses'
    courseId = dbsql.Column(dbsql.String(10), primary_key = True)
    name = dbsql.Column(dbsql.String, nullable = False)
    description = dbsql.Column(dbsql.String, nullable = False)
    department = dbsql.Column(dbsql.String, nullable = False)
    prerequisites = dbsql.Column(dbsql.String, nullable = False)
    course_level = dbsql.Column(dbsql.Integer, nullable=False)
    campus = dbsql.Column(dbsql.String, nullable=False)
    terms_offered = dbsql.Column(dbsql.String,  nullable=False)
    exclusion = dbsql.Column(dbsql.String, nullable=False)
    corequisites = dbsql.Column(dbsql.String, nullable=False)
    fase_available = dbsql.Column(dbsql.Boolean, nullable=False)

    def __repr__(self):
        return f"Course(Course Id: '{self.courseId}', Course Name: '{self.name}')"

class UserSavedCourses(Base):
    __tablename__ = 'user_saved_courses'
    userId = dbsql.Column(dbsql.Integer, ForeignKey('user.id'), primary_key = True) 
    courseId = dbsql.Column(dbsql.String(10), ForeignKey('courses.courseId'), primary_key = True)
    users = relationship("User")
    courses = relationship("Courses")
    def __repr__(self):
        return f"UserSavedCourses('User: {self.userId}', Saved Course: '{self.courseId}')"

class CourseComments(Base):
    __tablename__ = 'course_comments'
    userId = dbsql.Column(dbsql.Integer, ForeignKey('user.id'), primary_key = True)
    courseId = dbsql.Column(dbsql.String(15), ForeignKey('courses.courseId'), primary_key = True)
    comment = dbsql.Column(dbsql.String,primary_key = True)
    users = relationship("User")
    courses = relationship("Courses")

    def __repr__(self):
        return f"CourseComments(User: '{self.userId}', Course: '{self.courseId}', Comment: '{self.comment}')"

