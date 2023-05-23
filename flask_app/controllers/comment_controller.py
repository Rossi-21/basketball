from flask import render_template, request, flash, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from datetime import datetime
from flask_app.models.comment import Comment




@app.route('/comment/create/submit/<int:post_id>', methods=['POST'])
def submit_comment(post_id):
    if 'user_id' not in session:
        return redirect('/')

    content = request.form['content']
    user_id = session['user_id']
    
    if len(content) < 5:
        flash("Comment must have at least 5 characters")
        return redirect('/dashboard')

    data = {
        'content': content,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'user_id': user_id,
        'post_id': post_id
    }

    Comment.create_comment(data)

    return redirect('/dashboard')
