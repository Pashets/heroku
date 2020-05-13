import traceback

from flask import Blueprint, request, redirect, url_for
from flask import render_template
from .forms import ProjectForm
from flask_security import current_user

from app import db
from models import Post, Tag, User, Project
from flask_security import login_required

projects = Blueprint('projects', __name__, template_folder='templates', static_url_path='projects')


@projects.route('/')
@login_required
def index():
    return render_template('projects/index.html',
                           projects=User.query.filter(User.email == current_user.email).first().projects)


@projects.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity_participants = request.form['quantity_participants']
        # tags = []
        # all_to_add = []
        # for name in tags_name.split():
        #     tag = Tag.query.filter(Tag.name.contains(name)).first_or_404()
        #     if tag:
        #         tags += [tag]
        #         continue
        #     tag = Tag(name=name)
        #     all_to_add += [tag]
        #     tags += [tag]
        try:
            user = User.query.filter(User.email == current_user.email).first()
            project = Project(name=name, description=description, quantity_participants=quantity_participants,
                              created_by=str(user))
            # post.tags = tags
            # all_to_add.append(post)
            # db.session.add_all(all_to_add)
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
