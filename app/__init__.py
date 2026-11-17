import os
from flask import Flask
from dotenv import load_dotenv
from .pages import blueprint as pages_blueprint
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    SECRET_KEY = os.environ.get("SECRET_KEY")
    app.config.update(SECRET_KEY=SECRET_KEY)    
    
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY is not set. Copy .env.example to .env and fill it in.")
    
    app.register_blueprint(pages_blueprint)
    
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return None # temporary

    return app