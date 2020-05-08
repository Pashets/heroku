from app import app, User
from app import db
# print(User.__tablename__)
from posts.blueprint import posts

import view

app.register_blueprint(posts, url_prefix='/blog')

if __name__ == '__main__':
    app.run()

