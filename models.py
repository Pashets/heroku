import re
from datetime import datetime

from flask_security import UserMixin, RoleMixin, current_user

from app import db, login_manager


def slugify(s):
    pattern = r'[^\w+]'
    s = re.sub(pattern, '-', s).lower()
    for i in range(1, len(s)):
        if s[i] == s[i - 1] == '-':
            s = s[:i] + s[i + 1:]
    return s


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'{self.name}'


### Flask-Security ###

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )

user_projects = db.Table('user_projects',
                         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                         db.Column('project_id', db.Integer(), db.ForeignKey('project.id'))
                         )

project_tasks = db.Table('project_tasks',
                         db.Column('project_id', db.Integer(), db.ForeignKey('project.id')),
                         db.Column('task_id', db.Integer(), db.ForeignKey('task.id'))
                         )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    projects = db.relationship('Project', secondary=user_projects, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User: {self.id}, {self.email}>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    quantity_participants = db.Column(db.Integer)
    slug = db.Column(db.String(140), unique=True)
    created_by = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now)
    tasks = db.relationship('Task', secondary=project_tasks, backref=db.backref('projects', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return self.name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    slug = db.Column(db.String(140))
    state = db.Column(db.String(100), default='Создана')
    role = db.Column(db.String(100))
    deadline = db.Column(db.DateTime)
    artefacts = db.Column(db.String(255))
    user_email = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return self.title


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.create_all()
