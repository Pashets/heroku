import os


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgres://rxglppmizewiqn" \
                              ":a089876793044760d602d46ef27537f4de62c74ffcbcea8cd56cf55f4af4b0e7@ec2-54-197-34-207" \
                              ".compute-1.amazonaws.com:5432/d38ijngc9p36pb"
    SECRET_KEY = 'someting secret'

    ### Flask-security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    # SECURITY_REGISTERABLE = True

    SECURITY_LOGIN_USER_TEMPLATE = 'login.html'
    # SECURITY_REGISTER_USER_TEMPLATE= 'register.html'
    # SECURITY_RESET_PASSWORD_TEMPLATE = 'security/reset_password.html'
    # SECURITY_CHANGE_PASSWORD_TEMPLATE = 'security/change_password.html'
    # MAIL_SERVER = 'smtp.gmail.com',
    # MAIL_PORT = 587,
    # MAIL_USE_SSL = False,
    # MAIL_USERNAME = 'something',
    # MAIL_PASSWORD = 'xxxxxx',
    # MAIL_USE_TLS = True,
    # DEFAULT_MAIL_SENDER = 'Danny from DPC'
