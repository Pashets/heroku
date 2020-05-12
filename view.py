import traceback

import sqlalchemy
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from flask_security import current_user

from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, login_manager
from models import User, Role


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/myProjects')
@login_required
def startprpage():
    try:
        print(User.query.filter(User.email == current_user.email).first().projects)
    except:
        print(traceback.format_exc())
    return render_template('myProjects.html',
                           projects=User.query.filter(User.email == current_user.email).first().projects)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page or url_for('index'))
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (email or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        # elif email[0].isdigit():
        #     flash('Email must start with a letter!')
        else:
            try:
                user = User(email=email, password=password)
                role = Role.query.filter(Role.name == 'user').first()
                user.roles = [role]
                role.users += [user]
                # new_user = user_datastore.create_user(email=email, password=password)
                # role = Role.query.filter(Role.name == 'user').first()
                # user_datastore.add_role_to_user(new_user, role)
                db.session.add_all([user, role])
                db.session.commit()
                return redirect(url_for('login_page'))
            except IntegrityError:
                flash('This email already registered!')

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    # users = User.query.all()
    # role = Role.query.filter(Role.name == "user").first()
    # for user in users:
    #     if not user.roles:
    #         user_datastore.add_role_to_user(user, role)
    #     db
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(AttributeError)
# @app.register_error_handler
def catch_when_registration_end(e):
    return redirect(url_for('login_page'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None
