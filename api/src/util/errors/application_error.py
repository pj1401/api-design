class ApplicationError:
    def __init__(self, err: BaseException, message="An error occurred."):
        self.err = err


class UniqueViolationError(ApplicationError):
    def __init__(self, err, message="Duplicate key value violates unique constraint."):
        super().__init__(err, message)
