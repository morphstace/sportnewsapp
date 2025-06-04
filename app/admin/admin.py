from app.admin import bp
from app.forms import UserForm
from flask import render_template
from flask_login import login_required

@bp.route('/admin', methods=['GET'])
@login_required
def admin():
    form = UserForm()
    return render_template("admin.html", form=form)



