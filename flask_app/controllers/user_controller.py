from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')          
def index():
    return render_template("index.html") 

@app.route('/register', methods=['POST'])
def register():
    if user.User.validate_user(request.form):
        hashed_pass = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : hashed_pass
        }
        user_id = user.User.save(data)
        session["user_id"] = user_id
        return redirect('/dashboard')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    this_user = user.User.get_by_email(request.form)
    print(this_user)
    if this_user:
        if bcrypt.check_password_hash(this_user.password,request.form['password']):
            session['user_id'] = this_user.id
            return redirect('/dashboard')
    flash("Invalid Credentials", "logError")
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
