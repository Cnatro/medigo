import logging

from dotenv import load_dotenv
from flask_migrate import Migrate

from app.interfaces.routes.auth_routes import auth_bp

load_dotenv()
from flask import Flask

from app.config import Config
from app.infrastructure.db import db

migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.logger.setLevel(logging.INFO)
    app.config["SQLALCHEMY_ECHO"] = True
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    app.logger.info("App initialized")

    return app