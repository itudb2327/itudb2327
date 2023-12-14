from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, flash, render_template, redirect, url_for, session
from flask_login import UserMixin, login_user
import mysql.connector

class User(UserMixin):
    def __init__(self, id, username, password, status, joined):
        self.id = id
        self.username = username
        self.password = password
        self.status = status
        self.joined = joined
def add_user(db, username, password,status='user'):
    password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, password_hash, status) VALUES (%s, %s, %s)', (username, password_hash, status))
    db.commit()

def is_username_available(db, username):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    return cursor.fetchone() is None

def validate_login(db, username, password):
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password_hash'], password):
        return User(id=user['id'], username=user['username'], password=user['password_hash'], status=user['status'], joined=user['joined'])
    return None


def login_page(db):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if validate_user := validate_login(db, username, password):
            login_user(validate_user)
            flash('Login successful', 'success')
            return redirect(url_for('home'))  
        else:
            flash('Invalid username or password', 'error')

    return render_template("login.html")

def register_page(db):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_username_available(db, username):
            add_user(db, username, password)
            flash('Registration successful', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already taken', 'error')

    return render_template("register.html")
