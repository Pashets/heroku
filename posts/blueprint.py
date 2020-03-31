from flask import Blueprint
from flask import render_template
from models import Post, Tag

posts = Blueprint('posts', __name__, template_folder='templates', static_url_path='posts')


@posts.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if post:
        tags = post.tags
        return render_template('posts/post_detail.html', post=post, tags=tags)
    else:
        return "<h1>This post is not exist</h1>"


@posts.route('/tags')
def index_tag():
    tags = Tag.query.all()
    return render_template('posts/index_tag.html', tags=tags)


@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter_by(slug=slug).first()
    return render_template('posts/tag_detail.html', tag=tag, posts=tag.posts)
