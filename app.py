from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'some secret soup4533534453454'
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
