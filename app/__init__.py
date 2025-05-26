from flask import Flask
from app.news import bp as news_bp
from app.auth import bp as auth_bp
from app.users import bp as users_bp
from app.admin import bp as admin_bp
from app.extensions import db, login_manager, migrate
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    #Add CKEditor
    ckeditor = CKEditor(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Inizializza estensioni
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(news_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(admin_bp)
    
    return app
