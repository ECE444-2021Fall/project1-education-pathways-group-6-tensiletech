from types import MethodDescriptorType
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from app.courses.routes import course
from app.searching_filtering.forms import FilterForm, SearchForm
from flask_login import login_user, current_user, logout_user
from app import es

searching_filtering = Blueprint('searching_filtering', __name__)

@searching_filtering.route('/',methods=['GET','POST'])
def search_home():
    # Cannot log in if already logged in
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    search_form = SearchForm()
    filter_form = FilterForm()
    if request.method == 'POST':
        # check if filter_form is filled
        if search_form.search.data:
            search_word = search_form.data['keywords']
            if search_word == '':
                search_word = '__'
            # return performSearch(search_word=search_word, select=filter_form.data['select'], divisions=filter_form.data['divisions'], campuses=filter_form.data['campuses'])
            return redirect(url_for('searching_filtering.performSearch', search_word=search_word, select=filter_form.data['select'], divisions=filter_form.data['divisions'], campuses=filter_form.data['campuses']))
        if search_form.saved_courses.data:
            return redirect(url_for('courses.home'))
        if search_form.log_out.data:
            return redirect(url_for('users.logout'))
    return render_template('search.html', search_form=search_form, filter_form=filter_form)


@searching_filtering.route('/results/query?=<search_word>/<select>/<divisions>/<campuses>', methods=['GET', 'POST'])
# @searching_filtering.route('/results', methods=['GET', 'POST'])
def performSearch(search_word, select, divisions, campuses, top=5000):
    results_form = SearchForm()

    if results_form.saved_courses.data:
        return redirect(url_for('courses.home'))
    if results_form.log_out.data:
        return redirect(url_for('users.logout'))

    data = get_data(search_word, select, divisions, campuses, top)
    course_list = []
    for i in data['hits']['hits']:
        course_list.append(i['_source'])
    keys = []
    course_list_limited = []
    if course_list != None: 
        if len(course_list):
            keys = course_list[0].keys()
        course_list_limited = [{"Code": course["Code"], "Name": course["Name"], "Division" : course["Division"], \
            "Course Level" : course["Course Level"], "Campus" : course["Campus"]} for course in course_list]
    return render_template('searchresults.html', keys=list(keys), results_form=results_form, data=course_list_limited)

def get_data(search_word, select, divisions, campuses, top=5000):
    query_body = {
            "size": top,
            "query": {
                "bool": {
                }
            }
        }
    must = []
    if select != 'Any':
        query = {
            "match": {
                "Course Level": int(select)
            }
        }
        must.append(query)
    if divisions != 'Any':
        query = {
            "match": {
                "Division": divisions
            }
        }
        must.append(query)
    if campuses != 'Any':
        query = {
            "match": {
                "Campus": campuses
            }
        }
        must.append(query)
    if search_word != '__':
        query = {
            "multi_match": {
                "query": search_word,
                "fuzziness": "AUTO"
            }
        }
        must.append(query)
    query_body["query"]["bool"]["must"] = must
    return es.search(index="course_info_v2", body=query_body)
    return query_body
    
