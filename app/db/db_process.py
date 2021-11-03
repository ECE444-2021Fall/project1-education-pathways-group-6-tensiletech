from .db_models import *
from app import dbsql, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_course(course_id):
    return Courses.query.get(str(course_id))

def add_to_table(table_row):
    dbsql.session.add(table_row)
    dbsql.session.commit()

def querying_all(table):
    return table.query.all()

user1 = User(username = "romil", email = "romil.sjain@gmail.com", password = "password")
add_to_table(user1)
users = querying_all(User)
print(users)

course1 = Courses(courseId="ECE101", name="ece seminar", description="something", department="FASE", \
    prerequisites="ECE101 ECE928", course_level=4, campus="UTSG", terms_offered="Fall2020 Winter2021", exclusion="ECE410", \
        corequisites="ECE102", fase_available=True)
add_to_table(course1)
courses = querying_all(Courses)
print(courses)

userSavedCourse = UserSavedCourses(userId=1, courseId="ECE101")
add_to_table(userSavedCourse)
userSCs = querying_all(UserSavedCourses)
print(userSCs)

courseComment = CourseComments(userId=1, courseId="ECE101", comment="great course!")
add_to_table(courseComment)
courseComments = querying_all(CourseComments)
print(courseComments)

