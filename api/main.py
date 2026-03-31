import logging
import sys
from flask import Flask, g
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from api.src.db.connection_manager import DatabaseConnectionManager
from api.src.blueprints.users.routes import users_bp
from api.src.hooks.logging import setup_logging_hooks

load_dotenv()

JWT_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


def create_app():
    app = Flask(__name__)
    app.config.from_object("api.src.config.config")
    register_db_manager(app)
    register_blueprints(app)
    configure_logger(app)
    setup_logging_hooks(app)

    return app


def register_db_manager(app):
    """Register a database manager."""
    db_config = {
        "host": app.config["DB_HOST"],
        "database": app.config["DB_NAME"],
        "user": app.config["DB_USER"],
        "password": app.config["DB_PASSWORD"],
        "port": app.config["DB_PORT"],
    }
    db_manager = DatabaseConnectionManager(db_config)

    # Add db_manager to the application context, so it can be accessed during a request.
    @app.before_request
    def before_request():
        g.db_manager = db_manager


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(users_bp, url_prefix="/api")


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


if __name__ == "__main__":
    app = create_app()
    app.run()
