from app.auth import bp
from flask import render_template, redirect, url_for, flash, request
from app.models import User
from app.forms import LoginForm, UserForm, RegistrationForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("validating "+ form.username.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            print(login_user(user))
            return redirect(url_for('users.dashboard'))
        else: flash("Wrong username or password.")
    return render_template('login.html', form=form)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('news.news'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    name = None
    form = RegistrationForm()
    if form.validate_on_submit():
        user_by_mail = User.query.filter_by(email=form.email.data).first()
        user_by_name = User.query.filter_by(username=form.username.data).first()
        if user_by_mail is None and user_by_name is None:
            pw_hash = generate_password_hash(form.password.data, "pbkdf2:sha256")
            user = User(name=form.name.data, username=form.username.data, 
                email=form.email.data, password_hash=pw_hash)
            db.session.add(user)
            db.session.commit()
            flash("User registred successfully!")
            return redirect(url_for('auth.login'))
        else: flash("E-mail or username already in use!")
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
    our_users = User.query.order_by(User.date_added)
    return render_template("register.html",
         form = form, name=name,
         our_users=our_users)