from .db_models import *

# General Testing

# user1 = User(username = "keith", email = "keith@gmail.com", password = "keithb")
# add_to_table(user1)

# course1 = Courses(courseId="ECE101", name="ece seminar", description="something", department="FASE", \
#     prerequisites="ECE101 ECE928", course_level=4, campus="UTSG", terms_offered="Fall2020 Winter2021", exclusion="ECE410", \
#         corequisites="ECE102", fase_available=True)
# add_to_table(course1)

# userSavedCourse = UserSavedCourses(userId=1, courseId="ECE101")
# add_to_table(userSavedCourse)

# courseComment = CourseComments(userId=1, courseId="ECE101", comment="great course!")
# add_to_table(courseComment)

# Print out tables for verification

users = querying_all(User)
print(users)

courses = querying_all(Courses)
print(courses)

userSCs = querying_all(UserSavedCourses)
print(userSCs)

courseComments = querying_all(CourseComments)
print(courseComments)
