# from app import db
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for, session
from sqlalchemy.sql.sqltypes import VARBINARY
from app.courses.forms import CourseSearchForm
from app.courses.utils import filter_courses
from app import df, G
from app import es

courses = Blueprint('courses', __name__)
search = CourseSearchForm()

"""Homepage is essentially just the course search form. If a post request is received, call the method that finds search results."""
@courses.route('/',methods=['GET','POST'])
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
def course(code):

    #If the course code is not present in the dataset, progressively remove the last character until we get a match.
    #For example, if there is no CSC413 then we find the first match that is CSC41.
    #If there are no matches for any character, just go home.
    if code not in df.index:
        while True:
            code = code[:-1]
            if len(code) == 0:
                return redirect(url_for('courses.home'))
            t = df[df.index.str.contains(code)]
            if len(t) > 0:
                code = t.index[0]
                return redirect(url_for('courses.course'), code = code)


    course = df.loc[code]
    #use course network graph to identify pre and post requisites
    pre = G.in_edges(code)
    post = G.out_edges(code)

    excl = course['Exclusion']
    coreq = course['Corequisite']
    aiprereq = course['AIPreReqs']
    majors = course['MajorsOutcomes']
    minors = course['MinorsOutcomes']
    faseavailable = course['FASEAvailable']
    mayberestricted = course['MaybeRestricted']
    terms = course['Term']
    activities = course['Activity']
    course = {k:v for k,v in course.items() if k not in ['Course','Course Level Number','FASEAvailable','MaybeRestricted','URL','Pre-requisites','Exclusion','Corequisite','Recommended Preparation','AIPreReqs','MajorsOutcomes','MinorsOutcomes','Term','Activity'] and v==v}
    return render_template(
        'course.html',
        course=course,
        pre=pre, 
        post=post,
        excl=excl,
        coreq=coreq,
        aip=aiprereq,
        majors=majors,
        minors=minors,
        faseavailable=faseavailable,
        mayberestricted=mayberestricted,
        terms=terms,
        activities=activities,
        zip=zip
        )