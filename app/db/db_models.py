from app import dbsql, login_manager
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, String, DateTime, and_, delete
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin # Helps in managing a user session

class User(dbsql.Model, UserMixin):
    __tablename__ = 'user'
    id = dbsql.Column(dbsql.Integer, primary_key = True) # Generated automatically when not specified
    username = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    email = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    password = dbsql.Column(dbsql.String(100), nullable = False)

    def __repr__(self):
        return f"User(UserId: '{self.id}', Username: '{self.username}', email: '{self.email}')"
class Courses(dbsql.Model):
    __tablename__ = 'courses'
    courseId = dbsql.Column(dbsql.String(10), primary_key = True)
    name = dbsql.Column(dbsql.String, nullable = False)
    division = dbsql.Column(dbsql.String, nullable = False)
    description = dbsql.Column(dbsql.String, nullable = False)
    department = dbsql.Column(dbsql.String, nullable = False)
    prerequisites = dbsql.Column(dbsql.String, nullable = False)
    course_level = dbsql.Column(dbsql.Integer, nullable=False)
    utsc_breadth = dbsql.Column(dbsql.String, nullable = False)
    apsc_electives = dbsql.Column(dbsql.String, nullable = False)
    campus = dbsql.Column(dbsql.String, nullable=False)
    terms_offered = dbsql.Column(dbsql.String,  nullable=False)
    activity = dbsql.Column(dbsql.String, nullable = False)
    last_updated = dbsql.Column(dbsql.String, nullable = False)
    exclusion = dbsql.Column(dbsql.String, nullable=False)
    utm_distribution = dbsql.Column(dbsql.String, nullable=False)
    corequisites = dbsql.Column(dbsql.String, nullable=False)
    recommended_prep = dbsql.Column(dbsql.String, nullable=False)
    as_breadth = dbsql.Column(dbsql.String, nullable=False)
    as_distribution = dbsql.Column(dbsql.String, nullable=False)
    later_term_course_details = dbsql.Column(dbsql.String, nullable=False)
    course_hyperlink = dbsql.Column(dbsql.String, nullable=False)
    fase_available = dbsql.Column(dbsql.Boolean, nullable=False)
    maybe_restricted = dbsql.Column(dbsql.Boolean, nullable=False)
    major_outcomes = dbsql.Column(dbsql.String, nullable=False)
    minor_outcomes = dbsql.Column(dbsql.String, nullable=False)
    aip_rereqs = dbsql.Column(dbsql.String, nullable=False)

    def __repr__(self):
        return f"Course(Course Id: '{self.courseId}', Course Name: '{self.name}')"

class UserSavedCourses(dbsql.Model):
    __tablename__ = 'user_saved_courses'
    id = dbsql.Column(dbsql.Integer, primary_key = True)
    username = dbsql.Column(dbsql.String(100), unique = False, nullable = False)
    courseId = dbsql.Column(dbsql.String(10), ForeignKey('courses.courseId'))
    courses = relationship("Courses")
    def __repr__(self):
        return f"UserSavedCourses('User: {self.username}', Saved Course: '{self.courseId}')"

class CourseComments(dbsql.Model):
    __tablename__ = 'course_comments'
    id = dbsql.Column(dbsql.Integer, primary_key = True) # Generated automatically when not specified
    userId = dbsql.Column(dbsql.Integer, ForeignKey('user.id'))
    courseId = dbsql.Column(dbsql.String(15), ForeignKey('courses.courseId'))
    comment = dbsql.Column(dbsql.String)
    users = relationship("User")
    courses = relationship("Courses")

    def __repr__(self):
        return f"CourseComments(User: '{self.userId}', Course: '{self.courseId}', Comment: '{self.comment}')"

@login_manager.user_loader
def load_user(user_id):
    return dbsql.session.query(User).get(int(user_id))

def load_course(course_id):
    return dbsql.session.query(Courses).get(str(course_id))

def load_comments(course_id):
    return dbsql.session.query(CourseComments).filter_by(courseId=str(course_id)).all()

def load_saved_courses(username):
    return dbsql.session.query(UserSavedCourses).filter_by(username=username).all()

def add_to_table(table_row):
    dbsql.session.add(table_row)
    dbsql.session.commit()

def remove_course(username, course_id):
    dbsql.session.query(UserSavedCourses).filter(and_(UserSavedCourses.username == str(username), UserSavedCourses.courseId == str(course_id))).delete()
    dbsql.session.commit()

def isCourseSaved(username, course_id):
    saved = dbsql.session.query(UserSavedCourses).filter(and_(UserSavedCourses.username == str(username), UserSavedCourses.courseId == str(course_id))).one_or_none()
    print(f"Username is {username} and course_id is {course_id} and Result of isCourseSaved is {saved} \n")
    if saved == None:
        return False
    else:
        return True

def get_course_by_id(course_id):
    return dbsql.session.query(Courses).filter_by(courseId=course_id).one()


def querying_all(table):
    return dbsql.session.query(table).all()

def row_to_dict(row):
    result = dict()
    for col in row.__table__.columns:
        result[col.name] = str(getattr(row, col.name))
    return result
