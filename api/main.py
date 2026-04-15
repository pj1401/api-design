"""
The starting point of the API.
module: main.py
"""

import logging
import sys
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from api.src.config.config import create_config
from api.src.db.connection_manager import DatabaseConnectionManager
from api.src.blueprints.router import router_bp
from api.src.hooks.database import setup_database_hooks
from api.src.hooks.exception_handlers import setup_exception_handlers
from api.src.hooks.logging import setup_logging_hooks
from api.src.util.models.db_config import DbConfig

load_dotenv()


def create_app() -> Flask:
    """Set up the application."""
    app = Flask(__name__)
    config = create_config()
    print(config)
    app.config.from_object(config)
    register_db_manager(app)
    register_blueprints(app)
    register_exception_handlers(app)
    init_jwt_manager(app)
    configure_logger(app)

    return app


def register_db_manager(app: Flask) -> None:
    """Register a database manager."""
    print(app.config)
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


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    app.register_blueprint(router_bp)


def register_exception_handlers(app: Flask) -> None:
    """Register exception handlers."""
    setup_exception_handlers(app)


def init_jwt_manager(app: Flask) -> None:
    """Initialise JWT manager."""
    jwt = JWTManager(app)


def configure_logger(app: Flask) -> None:
    """Configure loggers."""
    set_logger_env(app)
    formatter = get_logger_formatter()
    remove_logger_handler(app)
    add_logger_handler(app, formatter)
    setup_logging_hooks(app)


def set_logger_env(app: Flask) -> None:
    """Determine environment and set logger level."""
    is_debug: bool = app.config["FLASK_DEBUG"].lower() in ("true", "1", "t")

    if is_debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)


def get_logger_formatter() -> logging.Formatter:
    """Get formatter for logger."""
    return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def remove_logger_handler(app: Flask) -> None:
    """Remove any existing handlers."""
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)


def add_logger_handler(app: Flask, formatter: logging.Formatter) -> None:
    """Add a new handler for console output."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)


if __name__ == "__main__":
    app = create_app()
    app.run()
