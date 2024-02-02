from flask import flash, redirect, render_template, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse as url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route("/")
@login_required
def index():
    posts = [{
             "author": { 'username': "nana"},
        "title": "first post",
        "body": "Beautiful day at the office"
    }]
    return render_template("index.html", title="Home", user=current_user, posts=posts)

@app.route("/signup", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You've signed up successfully!")
        return redirect(url_for("login"))

    return render_template("signup.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("index")
        return redirect(next_page)

    return render_template('login.html', title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
