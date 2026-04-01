from flask import request


def setup_logging_hooks(app):
    """Set up request and response logging hooks."""

    @app.before_request
    def log_request_info():
        app.logger.info(
            "Request: %s %s %s", request.method, request.path, request.remote_addr
        )

    @app.after_request
    def log_response_info(response):
        app.logger.info(
            "Response: %s %s %s", response.status_code, request.method, request.path
        )
        return response
