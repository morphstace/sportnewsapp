from models import Users, News
from . import login_manager

#Add DB
#OLD
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#NEW
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))