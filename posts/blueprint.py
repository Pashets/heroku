from flask import Blueprint
from flask import render_template
from flask_login import login_required

from models import Post, Tag

posts = Blueprint('posts', __name__, template_folder='templates', static_url_path='posts')


@posts.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
@login_required
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if post:
        tags = post.tags
        return render_template('posts/post_detail.html', post=post, tags=tags)
    else:
        return "<h1>This post is not exist</h1>"


@posts.route('/tags/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter_by(slug=slug).first()
    return render_template('posts/tag_detail.html', tag=tag, posts=tag.posts)


@posts.route('/tags')
@login_required
def index_tag():
    tags = Tag.query.all()
    return render_template('posts/index_tag.html', tags=tags)
