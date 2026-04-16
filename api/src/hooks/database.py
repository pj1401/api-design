"""
Set up hooks related to the database.
module: src/hooks/database.py
"""

from flask import Flask, g
from api.src.db.connection_manager import DatabaseConnectionManager


def setup_database_hooks(app: Flask, db_manager: DatabaseConnectionManager) -> None:
    """Add db_manager to the application context, so it can be accessed during a request."""

    @app.before_request
    def before_request() -> None:  # type: ignore[unused-ignore]
        g.db_manager = db_manager
