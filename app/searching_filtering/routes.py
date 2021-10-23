from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user

searching_filtering = Blueprint('searching_filtering', __name__)

@searching_filtering.route('/search',methods=['GET', 'POST'])
def search_home():
    # Cannot log in if already logged in
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    return render_template('landing.html', page="search")