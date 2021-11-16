# from app import db
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from app.courses.forms import CourseSearchForm
from app.courses.utils import filter_courses
from app.db.db_models import load_comments, load_course, row_to_dict, add_to_table, remove_course, CourseComments, UserSavedCourses, isCourseSaved, load_saved_courses, get_course_by_id
from app import df, G
from app import es

courses = Blueprint('courses', __name__)
search = CourseSearchForm()

"""Homepage is essentially just the course search form. If a post request is received, call the method that finds search results."""
@courses.route('/search',methods=['GET','POST'])
def home():
    search = CourseSearchForm(request.form)
    if request.method == 'POST':
        search_word = search.data['search']
        select = search.data['select']
        division = search.data['divisions']
        departments = search.data['departments']
        campuses = search.data['campuses']
        top = search.data['top']
        return redirect(url_for('courses.search_results', search_word=search_word, select=select, divisions=division, departments=departments, campuses=campuses, top=top))
        # return search_results(search)
    return render_template('index.html',form=search)


"""Handle the data from the POST request that will go to the main algorithm.
If we get an empty search, just go back to home.
Otherwise, pull out the elements of the POST request that are used by the algorithm, and get the results.
Then, render the results page with a list of pandas tables containing the results for each year.
Pass the original search to the template as well, so the user can see the context of what they asked for.
"""
@courses.route('/results/query=?q=<search_word>s=<select>d=<divisions>dp=<departments>c=<campuses>t=<top>')
@login_required
def search_results(search_word, select, divisions, departments, campuses, top):
    if search_word == '' or not search_word:
        return redirect(url_for('courses.home'))
    results = filter_courses(
        search_word,
        select,
        divisions,
        departments,
        campuses,
        top
        )
    
    return render_template('results.html',tables=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in results],form=search)

"""
This method shows the information about a single course.
First, some basic error handling for if a course is passed that does not exist.
Then, separate the course information into the elements which have specific display functionality and the rest, which we show in a big table.
Pass all that to render template.
"""
@courses.route('/course/<code>')
@login_required
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

    # checking if the course is saved for the user, need to pass to frontend to render
    # appropriate button
    isSaved = isCourseSaved(current_user.username, code)

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
        comments=comments,
        isSaved = isSaved
        )

@courses.route('/course/<code>/add_comment', methods=['POST'])
@login_required
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
# This method is used for both saving and unsaving courses
@courses.route('/course/<code>/save-course', methods = ['POST'])
@login_required
def save_course(code):
    # Validate if user has logged in
    if current_user and current_user.username:
        savedCourse = UserSavedCourses(username=current_user.username, courseId=code)

        if isCourseSaved(current_user.username, code):
            remove_course(current_user.username, code)
        else:
            add_to_table(savedCourse)
    else:
        print('User is not currently logged in')


    # Redirect back to the page originally called from
    if request.referrer:
        return redirect(request.referrer) 
    else:
        return redirect(url_for('courses.home'))


@courses.route('/course/my-courses', methods = ['GET'])
@login_required
def my_courses():

    all_user_courses = []
    if current_user and current_user.username:
        all_saved_courses = load_saved_courses(current_user.username)
        for i, course in enumerate(all_saved_courses):
            # print(f"i : {i} courseId: {course.courseId}")
            courseObj = get_course_by_id(course.courseId)
            # print(courseObj)
            if courseObj != None:
                all_user_courses.append(courseObj)
            else:
                print("Somehow the course object we got by id is null")

    return render_template('my-courses.html' , courses = all_user_courses)