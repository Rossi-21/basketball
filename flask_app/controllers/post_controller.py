from flask import render_template, request, flash, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment

@app.route('/dashboard')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({"id":session['user_id']})
    if not user:
        return redirect('/logout')
        
    return render_template('dashboard.html', user=user, posts=Post.get_all_posts())

@app.route('/posts/create')
def create_post():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return redirect('/dashboard')

@app.route('/post/create/submit', methods =['POST'])
def submit_post():
    if 'user_id' not in session:
        return redirect('/')
    if not Post.validate_new_post(request.form):
        return redirect('/posts/create')

    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    Post.save_post(data)
    return redirect('/dashboard')

@app.route('/profile/<int:id>')
def user_posts(id):
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_one({"id": id})
    if not user:
        return redirect('/logout')

    posts = Post.get_posts_by_user_id(user.id)

    for post in posts:
        post.comments = Comment.get_comments_by_post_id(post.id)

    return render_template("show_user.html", user=user, posts=posts)
