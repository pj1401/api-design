from flask import Flask, g
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from api.src.controllers.user_controller import UserController
from api.src.db.connection_manager import DatabaseConnectionManager
from api.src.repositories.user_repo import UserRepository
from api.src.services.user_service import UserService
from api.src.blueprints.users.routes import users_bp

load_dotenv()

JWT_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


def create_app():
    app = Flask(__name__)
    app.config.from_object("api.src.config.config")

    db_config = {
        "host": app.config["DB_HOST"],
        "database": app.config["DB_NAME"],
        "user": app.config["DB_USER"],
        "password": app.config["DB_PASSWORD"],
        "port": app.config["DB_PORT"],
    }
    db_manager = DatabaseConnectionManager(db_config)

    @app.before_request
    def before_request():
        g.db_manager = db_manager

    # Register blueprints
    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(users_bp, url_prefix="/api")


if __name__ == "__main__":
    app = create_app()
    app.run()
