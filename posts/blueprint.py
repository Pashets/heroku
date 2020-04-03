from flask import Blueprint, request, flash, redirect, url_for
from flask import render_template
from flask_login import login_required

from app import db
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


@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post(all_tags=Tag.query.all()):
    title = request.form.get('title')
    body = request.form.get('body')
    tags_string = request.form.get('tags')
    if title and body and tags_string:
        tags_string_list = tags_string.replace(' ', '').split(',')
        tags = []
        for name in tags_string_list:
            tags += [Tag.query.filter_by(name=name).first()]
        post = Post(title=title, body=body)
        post.tags = tags
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.index'))
    else:
        flash('Please fill title, body and tags fields')
    return render_template('posts/create_post.html', tags=all_tags)
