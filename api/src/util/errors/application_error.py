"""
Custom errors and helper functions.
module: src/util/errors/application_error.py
"""

import logging


class ApplicationError(Exception):
    def __init__(
        self, err: Exception | None = None, message: str = "An error occurred."
    ):
        self.err = err
        self.message = message


class UniqueViolationError(ApplicationError):
    def __init__(
        self,
        err: Exception,
        message: str = "Duplicate key value violates unique constraint.",
    ):
        super().__init__(err, message)


class InvalidCredentialsError(ApplicationError):
    def __init__(
        self,
        err: Exception | None = None,
        message: str = "Credentials invalid or not provided.",
    ):
        super().__init__(err, message)


class HttpError(ApplicationError):
    def __init__(
        self,
        err: Exception,
        status: int,
        message: str = "The server encountered an unexpected condition that prevented it from fulfilling the request.",
    ):
        super().__init__(err, message)
        self.status = status

    def to_dict(self) -> dict[str, int | str]:
        return {
            "status": self.status,
            "message": self.message,
        }


def convert_to_http_error(err: Exception) -> HttpError:
    error_name = type(err).__name__
    status = errorHttpStatusMap.get(error_name, 500)
    message = httpStatusReasonMap.get(
        status,
        "The server encountered an unexpected condition that prevented it from fulfilling the request.",
    )
    return HttpError(err, status, message)


errorHttpStatusMap = {
    "UniqueViolation": 400,
    "ValidationError": 400,
    "InvalidCredentialsError": 401,
}

httpStatusReasonMap = {
    400: "The request cannot or will not be processed due to something that is perceived to be a client error (for example validation error).",
    401: "Credentials invalid or not provided.",
    500: "The server encountered an unexpected condition that prevented it from fulfilling the request.",
}


def log_original_error(err: Exception):
    logging.error(f"Error occurred: {type(err).__name__}, Original exception: {err}")
