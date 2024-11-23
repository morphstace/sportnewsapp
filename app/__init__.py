from flask import Flask
from app.news import bp as news_bp
from app.auth import bp as auth_bp
from app.users import bp as users_bp
from app.extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password123@localhost/users'
    app.config['SECRET_KEY'] = "seckey"
    
    # Inizializza estensioni
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(news_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    
    return app
