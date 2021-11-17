from app import dbsql, login_manager
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, String, DateTime, and_, delete
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin # Helps in managing a user session

class User(dbsql.Model, UserMixin):
    """User Table

    """
    __tablename__ = 'user'
    id = dbsql.Column(dbsql.Integer, primary_key = True) # Generated automatically when not specified
    username = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    email = dbsql.Column(dbsql.String(100), unique = True, nullable = False)
    password = dbsql.Column(dbsql.String(100), nullable = False)

    def __repr__(self):
        return f"User(UserId: '{self.id}', Username: '{self.username}', email: '{self.email}')"
class Courses(dbsql.Model):
    """Courses Table

    """
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
    """UserSavedCourses Table

    """
    __tablename__ = 'user_saved_courses'
    id = dbsql.Column(dbsql.Integer, primary_key = True)
    username = dbsql.Column(dbsql.String(100), unique = False, nullable = False)
    courseId = dbsql.Column(dbsql.String(10), ForeignKey('courses.courseId'))
    courses = relationship("Courses")
    def __repr__(self):
        return f"UserSavedCourses('User: {self.username}', Saved Course: '{self.courseId}')"

class CourseComments(dbsql.Model):
    """Course Comments Table
    """
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
    """Querying User Table using user_id field

    Args:
        user_id (int): user_id of the user you want to query for

    Returns:
        User: User row object with attributes of the specific User querying for
    """
    return dbsql.session.query(User).get(int(user_id))

def load_course(course_id):
    """Querying Courses Table using course_id field 

    Args:
        course_id (string): Course Code you want all the attributes for

    Returns:
        Courses: Courses row object with attributes of the specific Course querying for
    """
    return dbsql.session.query(Courses).get(str(course_id))

def load_comments(course_id):
    """Querying the Comments table using the course_id

    Args:
        course_id (string): Course code of the course comments querying for

    Returns:
        [CourseComments]: List of CourseComment rows associated with the course_id
    """
    return dbsql.session.query(CourseComments).filter_by(courseId=str(course_id)).all()

def load_saved_courses(username):
    """
    Args:
        username (string): username of the user that you want to query the saved courses

    Returns:
        [UserSavedCourses]: List of UserSavedCourses rows associated with the username
    """
    return dbsql.session.query(UserSavedCourses).filter_by(username=username).all()

def add_to_table(table_row):
    """Adding a row to any of the DB Tables

    Args:
        table_row (DB Class): A DB Model class to be added in as a row to the associated DB Table
    """
    dbsql.session.add(table_row)
    dbsql.session.commit()

def remove_course(username, course_id):
    """Unsaving a specified course for the specified user

    Args:
        username (string): username of the user 
        course_id (string): course_id of the course needing to be unsaved for the user
    """
    dbsql.session.query(UserSavedCourses).filter(and_(UserSavedCourses.username == str(username), UserSavedCourses.courseId == str(course_id))).delete()
    dbsql.session.commit()

def isCourseSaved(username, course_id):
    """Checking if a course is saved for a specific user

    Args:
        username (string): username of the user
        course_id (string): course_id of the course needing to be unsaved for the user

    Returns:
        Bool: False if course is not saved under the specified user, True otherwise
    """
    saved = dbsql.session.query(UserSavedCourses).filter(and_(UserSavedCourses.username == str(username), UserSavedCourses.courseId == str(course_id))).one_or_none()
    # print(f"Username is {username} and course_id is {course_id} and Result of isCourseSaved is {saved} \n")
    if saved == None:
        return False
    else:
        return True

def get_course_by_id(course_id):
    """Querying Courses Table using course_id field another methodology from load_course

    Args:
        course_id (string): Course Code you want all the attributes for

    Returns:
        Courses: Courses row object with attributes of the specific Course querying for
    """
    return dbsql.session.query(Courses).filter_by(courseId=str(course_id)).one_or_none()


def querying_all(table):
    """Returning all the rows of any DB Table

    Args:
        table (DB Class): Specified table querying for all the entries

    Returns:
        [DB Class]: List of all entries of "table" row objects
    """
    return dbsql.session.query(table).all()

def row_to_dict(row):
    """Table row object conversion to a dictionary of its fields

    Args:
        row (Table row): Table class row wanted to be converted to a dictionary

    Returns:
        Dict : Specified Table row's attributes returned as a dictionary
    """
    result = dict()
    for col in row.__table__.columns:
        result[col.name] = str(getattr(row, col.name))
    return result