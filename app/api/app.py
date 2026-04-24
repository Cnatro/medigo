import logging
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


from app.interfaces.routes.auth_routes import auth_bp
from app.interfaces.routes.clinic_routes import clinic_bp
from app.interfaces.routes.doctor_routes import doctor_bp
from app.interfaces.routes.order_routes import order_bp
from app.interfaces.routes.specialty_routes import specialty_bp
from app.interfaces.routes.time_slot_routes import time_slot_bp
from app.interfaces.routes.user_routes import user_bp

load_dotenv()
from flask import Flask

from app.config import Config
from app.infrastructure.db import db

migrate = Migrate()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/api/*": {"origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://medigo-ui.onrender.com"
        ]}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Content-Type", "Authorization"]
    )
    app.config.from_object(Config)

    app.logger.setLevel(logging.INFO)
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)
    JWTManager(app)

    migrate.init_app(app, db)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
    app.register_blueprint(clinic_bp, url_prefix="/api/clinics")
    app.register_blueprint(specialty_bp, url_prefix="/api/specialties")
    app.register_blueprint(time_slot_bp, url_prefix="/api/time_slots")

    app.logger.info("App initialized")

    return app
