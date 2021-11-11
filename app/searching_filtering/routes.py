from types import MethodDescriptorType
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from app.courses.routes import course
from app.searching_filtering.forms import FilterForm, SearchForm
from flask_login import login_user, current_user, logout_user
from app import es

searching_filtering = Blueprint('searching_filtering', __name__)

@searching_filtering.route('/search',methods=['GET','POST'])
def search_home():
    print("Entering search home")
    # Cannot log in if already logged in
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    search_form = SearchForm()
    filter_form = FilterForm()
    print("search form: ", search_form.data)
    print("filter form: ", filter_form.data)
    if request.method == 'POST':
        print("search===========")
        # check if filter_form is filled
        if search_form.search.data:
            return performSearch(search_form, filter_form)
        if search_form.saved_courses.data:
            return redirect(url_for('courses.home'))
        if search_form.log_out.data:
            return redirect(url_for('users.logout'))
    return render_template('search.html', search_form=search_form, filter_form=filter_form)
    # return render_template('index.html', form=search_form)


@searching_filtering.route('/results')
def performSearch(search_form, filter_form=None, methods=['GET', 'POST']):
    query = None
    results_form = SearchForm()

    if results_form.saved_courses.data:
        return redirect(url_for('courses.home'))
    if results_form.log_out.data:
        return redirect(url_for('users.logout'))

    if request.method == 'POST':
        query = search_form.data['keywords']
    print("Query keywords: ", query)
    if query == '':
        data = es.search(index="course_info")
    else:
        data = es.search(index="course_info", body={"query": {
            "multi_match": {
                "query": query,
                "fuzziness": "AUTO"
            }
        }})
    course_list = []
    for i in data['hits']['hits']:
        course_list.append(i['_source'])
    print(course_list)
    keys = []
    course_list_cd = []
    if course_list != None: 
        if len(course_list):
            keys = course_list[0].keys()
        course_list_cd = [{"Code": course["Code"], "Name": course["Name"]} for course in course_list]
        print(course_list_cd)
    return render_template('searchresults.html', keys=list(keys), results_form=results_form, data=course_list_cd)
