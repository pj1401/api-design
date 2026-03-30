class ApplicationError:
    def __init__(self, err: BaseException, message="An error occurred."):
        self.err = err
        self.message = message


class UniqueViolationError(ApplicationError):
    def __init__(
        self,
        err: BaseException,
        message="Duplicate key value violates unique constraint.",
    ):
        super().__init__(err, message)


class HttpError(ApplicationError):
    def __init__(
        self,
        err: BaseException,
        status: int,
        message="The server encountered an unexpected condition that prevented it from fulfilling the request.",
    ):
        super().__init__(err, message)
        self.status = status


def convert_to_http_error(err: BaseException) -> HttpError:
    status = errorHttpStatusMap[type(err).__name__] if isinstance(err, BaseException) else 500
    return HttpError(err, status, httpStatusReasonMap[status])


errorHttpStatusMap = {
    "UniqueViolation": 400,
}

httpStatusReasonMap = {
    400: "The request cannot or will not be processed due to something that is perceived to be a client error (for example validation error)."
}
