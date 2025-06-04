from flask import Flask
from app.news import bp as news_bp
from app.auth import bp as auth_bp
from app.users import bp as users_bp
from app.admin import bp as admin_bp
from app.extensions import db, migrate
from flask_ckeditor import CKEditor
from app.extensions import login_manager
from flask_security import Security, SQLAlchemyUserDatastore
from app.forms import LoginForm
from app.models import User, Role
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    #Add CKEditor
    ckeditor = CKEditor(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SECURITY_DEFAULT_BLUEPRINT'] = False
    app.config['SECURITY_LOGIN_URL'] = '/login'

    
    # Inizializza estension
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    
    app.register_blueprint(news_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(admin_bp)
    
    security = Security(app, user_datastore)
    
    return app
