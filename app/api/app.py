import logging

from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()
from flask import Flask

from app.config import Config
from app.infrastructure.db import db

migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        try:
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))

            app.logger.info("Connected to PostgreSQL successfully")

        except Exception as e:
            app.logger.error(f"DB Connection failed: {str(e)}")

    return app