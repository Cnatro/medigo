import logging

from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.interfaces.routes.auth_routes import auth_bp
from app.interfaces.routes.order_routes import order_bp
from app.interfaces.routes.user_routes import user_bp

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
    JWTManager(app)

    migrate.init_app(app, db)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(order_bp, url_prefix="/api/orders")

    app.logger.info("App initialized")

    return app