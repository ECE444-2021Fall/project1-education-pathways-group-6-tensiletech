from app import bcrypt
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from app.db.db_models import User
from app.db.db_process import add_user
from app.users.forms import LoginForm, CreateForm
from flask_login import login_user, current_user, logout_user

users = Blueprint('users', __name__)

@users.route('/login',methods=['GET', 'POST'])
def login():

    # Cannot log in if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('courses.home'))

    form = LoginForm()
    if form.validate_on_submit():

        # Check user credentials
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Logs the user in and redirects to home page
            login_user(user) # can also add remember me argument here if we add remember me input in form

            # If user was trying to access a page but was redirected to login before accessing
            # we need to redirect him to that page again
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('courses.home'))
        else:
            # print("incorrect credentials")
            flash('Incorrect username or password, please try again', 'danger')

    return render_template('landing.html', form=form, page="login")

@users.route('/signup',methods=['GET', 'POST'])
def create():

    # Cannot create account if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('courses.home'))
    
    form = CreateForm()
    if form.validate_on_submit():

        # Create user credentials
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, password = hashed_password, email = form.email.data)

        # Add the user to the database
        add_user(user)
        
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('landing.html', form=form, page="create")

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))