from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
import sqlalchemy as sa
from app import app, db
from app.models import User
from app.forms import LoginForm, RegisterForm

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user == None or user.check_password(form.password.data):
            flash("Incorrect email or password.")
            return redirect(url_for('home'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/main')
@login_required
def main():
    return render_template('main.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))