import traceback

from flask import Blueprint, request, redirect, url_for
from flask import render_template
from .forms import ProjectForm, TaskForm
from flask_security import current_user

from app import db
from models import Post, Tag, User, Project, Task
from flask_security import login_required

projects = Blueprint('projects', __name__, template_folder='templates', static_url_path='projects')


@projects.route('/')
@login_required
def index():
    """Index function, which return index project page """

    return render_template('projects/index.html',
                           projects=User.query.filter(User.email == current_user.email).first().projects)


@projects.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    """Create project function, which return form to create project"""

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity_participants = request.form['quantity_participants']
        try:
            user = User.query.filter(User.email == current_user.email).first()
            project = Project(name=name, description=description, quantity_participants=quantity_participants,
                              created_by=user.email)
            user.projects.append(project)
            db.session.add_all([project, user])
            db.session.commit()
            return redirect(url_for('projects.index'))
        except:
            print('Something went wrong')
            print(traceback.format_exc())
            return '<h1>Something went wrong<h1>' + traceback.format_exc()
    form = ProjectForm()
    return render_template('projects/create_project.html', form=form)


@projects.route('/<slug>')
def project_info(slug):
    """Project info, which return info page to this project"""

    project = Project.query.filter(Project.slug == slug).first_or_404()
    if project:
        return render_template('projects/project_info.html', project=project)
    else:
        return "<h1>This project is not exist</h1>"


@projects.route('/<slug>/tasks')
def tasks(slug):
    project = Project.query.filter(Project.slug == slug).first_or_404()
    if project:
        return render_template('projects/project_tasks.html', project=project)
    else:
        return "<h1>This project is not exist</h1>"


# Печалька!
@projects.route('/<slug>/tasks/<slug_task>', methods=['GET', 'POST'])
@login_required
def task_detail(slug, slug_task):
    project = Project.query.filter(Project.slug == slug).first_or_404()
    tasks = project.tasks
    task = False
    for i in tasks:
        if i.slug == slug_task:
            task = i

    if request.method == 'POST':
        try:
            task = Task.query.filter(Task.slug == slug_task).first()
            task.user_email = current_user.email
            db.session.add(task)
            db.session.commit()
        except:
            print(traceback.format_exc())

    if project and task:
        artefacts_string: str = task.artefacts
        artefacts = artefacts_string.split()
        return render_template('projects/task_detail.html', project=project, task=task, artefacts=artefacts)
    else:
        return "<h1>This project or/and task is/are not exist</h1>"


@projects.route('/<slug>/users', methods=['GET', 'POST'])
def users(slug):
    project = Project.query.filter(Project.slug == slug).first_or_404()

    if request.method == 'POST':
        try:
            if current_user.is_anonymous:
                return redirect(url_for('login_page') + '?next=' + request.url)

            if len(project.users.all()) < project.quantity_participants:
                user = User.query.filter(User.email == current_user.email).first()
                user.projects += [project]
                db.session.add(user)
                db.session.commit()
        except:
            print(traceback.format_exc())
    if project:
        return render_template('projects/project_users.html', project=project)
    else:
        return "<h1>This project is not exist</h1>"


@projects.route('/<slug>/create_task', methods=['GET', 'POST'])
def create_task(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        role = request.form['role']
        deadline = request.form['deadline']
        artefacts = request.form['artefacts']
        try:
            task = Task(title=title, description=description, role=role, deadline=deadline, artefacts=artefacts)
            project.tasks.append(task)
            db.session.add_all([project, task])
            db.session.commit()
            return redirect(url_for('projects.tasks', slug=project.slug))
        except:
            print('Something went wrong')
            print(traceback.format_exc())
            return '<h1>Something went wrong<h1>' + traceback.format_exc()
    form = TaskForm()
    return render_template('projects/create_task.html', form=form, project=project)


@projects.route('/all_projects')
def all_projects():
    projects = Project.query.all()
    return render_template('projects/all_projects.html', projects=projects)
