import os


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgres://rxglppmizewiqn" \
                              ":a089876793044760d602d46ef27537f4de62c74ffcbcea8cd56cf55f4af4b0e7@ec2-54-197-34-207" \
                              ".compute-1.amazonaws.com:5432/d38ijngc9p36pb"
