import os

from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager

from .pages import blueprint as pages_blueprint
from .extensions import db, migrate

login_manager = LoginManager()

def secret_key():
    key = os.environ.get("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY is not set. Copy .env.example to .env and fill it in.")
    return key

def database_url():
    url = os.environ.get("DATABASE_URL")
    if not url:
        return "sqlite:///cinematch.db"
    return url
    
def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    app.config.update(
        SECRET_KEY = secret_key(),
        SQLALCHEMY_DATABASE_URI=database_url(),
        SQLALCHEMY_ENGINE_OPTIONS={"pool_pre_ping": True, "pool_recycle": 300},
    )
    
    app.register_blueprint(pages_blueprint)
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return None # temporary

    return app