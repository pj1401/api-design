import logging
import sys
from flask import Flask
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from api.src.db.connection_manager import DatabaseConnectionManager
from api.src.blueprints.router import router_bp
from api.src.hooks.database import setup_database_hooks
from api.src.hooks.exception_handlers import setup_exception_handlers
from api.src.hooks.logging import setup_logging_hooks
from api.src.util.models.db_config import DbConfig

load_dotenv()

JWT_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


def create_app():
    """Set up the application."""
    app = Flask(__name__)
    app.config.from_object("api.src.config.config")
    register_db_manager(app)
    register_blueprints(app)
    register_exception_handlers(app)
    configure_logger(app)

    return app


def register_db_manager(app):
    """Register a database manager."""
    db_manager = DatabaseConnectionManager(
        DbConfig(
            app.config["DB_HOST"],
            app.config["DB_NAME"],
            app.config["DB_USER"],
            app.config["DB_PASSWORD"],
            app.config["DB_PORT"],
        )
    )
    setup_database_hooks(app, db_manager)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(router_bp)


def register_exception_handlers(app):
    """Register exception handlers."""
    setup_exception_handlers(app)


def configure_logger(app):
    """Configure loggers."""
    set_logger_env(app)
    formatter = get_logger_formatter()
    remove_logger_handler(app)
    add_logger_handler(app, formatter)
    setup_logging_hooks(app)


def set_logger_env(app):
    """Determine environment and set logger level."""
    is_debug = app.config["FLASK_DEBUG"].lower() in ("true", "1", "t")

    if is_debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)


def get_logger_formatter():
    """Get formatter for logger."""
    return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def remove_logger_handler(app):
    """Remove any existing handlers."""
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)


def add_logger_handler(app, formatter):
    """Add a new handler for console output."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)


if __name__ == "__main__":
    app = create_app()
    app.run()
