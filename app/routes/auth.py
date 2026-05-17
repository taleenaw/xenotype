from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
import re

def is_valid_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    return True, ""

def is_valid_username(username):
    if not username:
        return False, "Username is required."

    if len(username) < 3:
        return False, "Username must be at least 3 characters long."

    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."

    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False, "Username can only contain letters, numbers, and underscores."

    return True, ""


def is_valid_email(email):
    if not email:
        return False, "Email is required."

    if len(email) > 120:
        return False, "Email must be no more than 120 characters long."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Enter a valid email address."

    return True, ""

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        is_valid, error_message = is_valid_username(username)

        if not is_valid:

            flash(error_message)

            return redirect(url_for('auth.register'))

        is_valid, error_message = is_valid_email(email)

        if not is_valid:

            flash(error_message)

            return redirect(url_for('auth.register'))
        
        is_valid, error_message = is_valid_password(password)

        if not is_valid:
            flash(error_message)
            
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))

        email_check = User.query.filter_by(email=email).first()
        if email_check:
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('auth.register'))

        

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):

            flash('Incorrect username or password.')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('main.lobby'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
