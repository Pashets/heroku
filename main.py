from app import app, User
from app import db

from posts.blueprint import posts
from projects.blueprint import projects

import view

app.register_blueprint(posts, url_prefix='/blog')
app.register_blueprint(projects, url_prefix='/projects')

if __name__ == '__main__':
    app.run()

