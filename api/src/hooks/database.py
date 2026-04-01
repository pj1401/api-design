from flask import g


def setup_database_hooks(app, db_manager):
    """Add db_manager to the application context, so it can be accessed during a request."""

    @app.before_request
    def before_request():
        g.db_manager = db_manager
