from app.users import bp
from flask import render_template, flash, request
from flask_login import login_required, current_user
from app.models import User
from app.forms import UserForm
from app.extensions import db

@bp.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    form = UserForm()
    name = None
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully.")
        our_users = User.query.order_by(User.date_added)
        return render_template("add_user.html",
            form=form, name=name, our_users=our_users)
    except:
        flash("Exception occured!")
    our_users = User.query.order_by(User.date_added)
    return render_template("register.html",
        name=name,
        our_users=our_users,
        form=form)

#Update DB record
@bp.route('/update/<int:id>', methods =['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    ## preventing modification from other user
    if id != current_user.id:
        return render_template("update.html",
                form = form,
                name_to_update = User.query.get_or_404(current_user.id), id=current_user.id)
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("update.html",
                form = form,
                name_to_update = name_to_update, id=id)
        except:
            flash("Error in updating user.")
    return render_template("update.html",
                form = form,
                name_to_update = name_to_update, id=id)

@bp.route('/user/<name>')
def user(name):
    #return "TEST"
    return render_template("add_user.html", name=name)

#dashboard
@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    user_id = current_user.id
    name_to_update = User.query.get_or_404(user_id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("dashboard.html",
                form = form,
                name_to_update = name_to_update)
        except:
            flash("Error in updating user.")
    return render_template("dashboard.html",
                form = form,
                name_to_update = name_to_update)