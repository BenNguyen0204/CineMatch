"""CineMatch application factory."""
import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"

# Wrap in a function so that we can create multiple instances of the app for testing
def create_app():
    app = Flask(__name__) # App name will be app
    
    # Reads SECRET_KEY from .env, Flask uses it to sign session cookies
    # app.config is used to store central application
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    
    # Neon closes idle connections, so test each one before reusing it.
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Imported here because both modules import `db` from this package.
    from . import models
    from .routes import main

    app.register_blueprint(main)

    return app
