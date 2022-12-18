from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.form
        user_login = data.get('login')
        password = data.get('password')
        user = User.query.filter_by(login=user_login).first()
        if not user or not check_password_hash(user.password, password):
            flash('Incorrect username/password', category='danger')
            return render_template('login.html')
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        data = request.form
        user_login = data.get('login')
        full_name = data.get('fullname')
        password1 = data.get('password1')
        password2 = data.get('password2')
        if User.query.filter_by(login=user_login).first():
            flash('This login already exists.', category='danger')
        elif user_login.find(' ') != -1:
            flash('Login may not contain white spaces.', category='danger')
        elif len(user_login) < 4:
            flash('Login must be greater than 3 characters.', category='danger')
        elif len(full_name) < 2:
            flash('Full name must be greater than 1 character.', category='danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='danger')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='danger')
        else:
            new_user = User(
                login=user_login,
                full_name=full_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template('sign_up.html')
