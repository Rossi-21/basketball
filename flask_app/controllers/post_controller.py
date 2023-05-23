import os
from flask import render_template, request, flash, redirect, session, make_response, send_from_directory, send_file
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from werkzeug.utils import secure_filename

#Image Extensions We accept
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'} 

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Home Page
@app.route('/dashboard')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('dashboard.html', user=user, posts=Post.get_all_posts())

#Create Post View
@app.route('/posts/create')
def create_post():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('new_post.html', user=user, posts=Post.get_all_posts())

#Create Post Method Includes Image Upload
@app.route('/post/create/submit', methods = ['POST'])
def submit_post():
    if 'user_id' not in session:
        return redirect('/')
    
    filename = "" #default

    if 'image_path' in request.files:
        file = request.files['image_path']
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.abspath(app.config['UPLOAD_FOLDER'] + filename))
    
    data = {
        'user_id': session['user_id'],
        'content': request.form['content'],
        'image_path': filename
    }
    if not Post.validate_new_post(data):
        return redirect('/posts/create')
    Post.save_post(data)
    return redirect('/dashboard')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

#Update View
@app.route('/posts/edit/<int:post_id>')
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    data ={
        'id' : post_id
    }
    return render_template('edit_post.html', user=user, post=Post.get_post_by_id(data))

#Update Method
@app.route('/posts/edit/submit/<int:post_id>', methods = ['POST'])
def submit_edit_post(post_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : post_id,
        'user_id': session['user_id'],
        'content': request.form['content']
    }

    Post.update_post(data)
    return redirect('/dashboard')

#User View
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

#Post View
@app.route('/show/post/<int:id>')
def show_post(id):
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_one({"id": session['user_id']})
    if not user:
        return redirect('/logout')

    data = {
        'id': id
    }

    post = Post.get_one_post(data)

    return render_template("show_post.html", user=user, post=post)

#Route that returns an image from the Folder
@app.route('/get_image/<int:id>')
def get_image(id):
    post = Post.get_one_post({'id': id})
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image_path)
    response = make_response(send_file(image_path))
    response.headers['Content-Type'] = 'image/jpeg'
    return response

#Delete Post Method
@app.route('/delete/post/<int:post_id>')
def destroy(post_id):
    data ={
        'id': post_id
    }
    Post.delete_post(data)
    return redirect('/dashboard')