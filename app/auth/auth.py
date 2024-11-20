from app.auth import bp
from flask import render_template, redirect, url_for, flash, request
from app.models import Users
from app.forms import LoginForm, UserForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('users.dashboard'))
            else: flash("Wrong username or password.")
        else: flash("Wrong username or password.")
    return render_template('login.html', form=form)

#logout
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('news.news'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            pw_hash = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(name=form.name.data, username=form.username.data, 
                email=form.email.data, password_hash=pw_hash)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        flash("User registred successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("register.html",
         form = form, name=name,
         our_users=our_users)