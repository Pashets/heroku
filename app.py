from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user
from flask import redirect, url_for, request

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

# from sqlalchemy import text
#
# sql = text('alter table "user" auto_increment=1')
# result = db.engine.execute(sql)
# names = [row[0] for row in result]
# print(names)

migrate = Migrate(app, db)

login_manager = LoginManager(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### Admin ###
from models import *


class AdminMixin:
    """Class AdminMixin for admin panel"""

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    """Class BaseModelView for admin panel"""

    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    """Class AdminView for admin panel"""

    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    """Class HomeAdminView for admin panel"""

    pass


class PostAdminView(AdminMixin, BaseModelView):
    """Class PostAdminView for admin panel"""

    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    """Class TagAdminView for admin panel"""

    form_columns = ['name', 'posts']


class ProjectAdminView(AdminMixin, BaseModelView):
    """Class ProjectAdminView for admin panel"""

    form_columns = ['name', 'description', 'users', 'slug', 'created_by', 'created']


class TaskAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'description', 'state', 'slug', 'role', 'created', 'deadline', 'artefacts', 'user_email']


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(ProjectAdminView(Project, db.session))
admin.add_view(TaskAdminView(Task, db.session))

### Flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
