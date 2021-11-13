# from app import db
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from app.courses.forms import CourseSearchForm
from app.courses.utils import filter_courses
from app.db.db_models import load_course, load_comments, row_to_dict, add_to_table, remove_course, CourseComments, UserSavedCourses, isCourseSaved
from app import df, G

courses = Blueprint('courses', __name__)

"""Homepage is essentially just the course search form. If a post request is received, call the method that finds search results."""
@courses.route('/',methods=['GET','POST'])
@login_required
def home():
    search = CourseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html',form=search)


"""Handle the data from the POST request that will go to the main algorithm.
If we get an empty search, just go back to home.
Otherwise, pull out the elements of the POST request that are used by the algorithm, and get the results.
Then, render the results page with a list of pandas tables containing the results for each year.
Pass the original search to the template as well, so the user can see the context of what they asked for.
"""
@courses.route('/results')
def search_results(search):
    if search.data['search'] == '' or not search.data['search']:
        return redirect(url_for('courses.home'))
    results = filter_courses(
        search.data['search'],
        search.data['select'],
        search.data['divisions'],
        search.data['departments'],
        search.data['campuses'],
        search.data['top']
        )

    return render_template('results.html',tables=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in results],form=search)

"""
This method shows the information about a single course.
First, some basic error handling for if a course is passed that does not exist.
Then, separate the course information into the elements which have specific display functionality and the rest, which we show in a big table.
Pass all that to render template.
"""
@courses.route('/course/<code>')
def course(code):
    course_info = load_course(code)

    if not course_info:
        return redirect(url_for('courses.home'))

    pre = list(filter(None, course_info.prerequisites.strip(' ').split(' ')))
    coreq = list(filter(None, course_info.corequisites.strip(' ').split(' ')))
    excl = list(filter(None, course_info.exclusion.strip(' ').split(' ')))
    terms = []
    for term in course_info.terms_offered.split(' '):
        if term.isnumeric() or len(terms) == 0:
            terms.append(term)
        else:
            terms[-1] += ' ' + term
    
    commentsQuery = load_comments(code)
    comments = []
    for c in commentsQuery:
        comments.append(row_to_dict(c))

    return render_template(
        'course.html',
        code=code,
        name=course_info.name,
        description=course_info.description,
        level=course_info.course_level,
        campus=course_info.campus,
        division=course_info.division,
        department=course_info.department,
        pre=pre,
        excl=excl,
        coreq=coreq,
        terms=terms,
        comments=comments
        )

@courses.route('/course/<code>/add_comment', methods=['POST'])
def add_comment(code):

    # Make sure that comment is not empty
    if not any(c.isalpha() for c in request.form['text']):
        return redirect(url_for('courses.course', code = code))

    # Make sure user is logged in before he tries to comment
    if current_user and current_user.username:
        comment = CourseComments(
            userId=current_user.username,
            courseId=code,
            comment=request.form['text']
        )
        add_to_table(comment)
    else:
        print('User is not currently logged in')
    
    return redirect(url_for('courses.course', code = code))

# When this function is called from the search page, the argument needs to be passed. Eg:
        #   <form action="{{ url_for('courses.save_course', course_id = course.id) }}" method="POST">
        #     <input class="btn" type="submit" value="Save">
        #   </form>
# But above, the value should say either save or unsave based on condition if course is already saved or not
# This route is called from both the search page and the course info page
# The route needs to redirect back to the page that it was actually called from
# This method is used for both saving and unsaving courses
@courses.route('/course/<code>/save-course', methods = ['POST'])
def save_course(code):
    
    # Validate if user has logged in
    if current_user and current_user.username:
        savedCourse = UserSavedCourses(username=current_user.username, courseId=code)

        if isCourseSaved(current_user.username, code):
            remove_course(current_user.username, code)
            print("Course was already saved!")
        else:
            add_to_table(savedCourse)
            print("Course was saved!")
    else:
        print('User is not currently logged in')


    # Redirect back to the page originally called from
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)
    else:
        return redirect(url_for('courses.course', code = code)) 

