from crypt import methods
from flask_app.models.user import User
from flask_app import app
from flask import render_template, jsonify, request, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login')
def get_login():
    return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id']
    }
    User.get_one(data)
    return render_template('dashboard.html', user = User.get_one(data))

@app.route('/submit_hours', methods=['POST'])
def submit_hours():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id'],
        "hours" : request.form['hours']
    }
    User.update_hours(data)
    return redirect('/pay')

@app.route('/pay')
def get_pay():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('pay.html')

@app.route('/submit_pay', methods=['POST'])
def submit_pay():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id'],
        "pay" : request.form['pay']
    }
    User.update_pay(data)
    return redirect('/clock')

@app.route('/clock')
def get_clock():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id']
    }
    return render_template('clock.html', user = User.get_one(data))

@app.route('/reset')
def reset():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id'],
    }
    User.reset(data)
    return redirect('/dashboard')