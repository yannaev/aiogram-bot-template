class AppException(Exception):
    message = "Неожиданная ошибка"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class ObjectAlreadyExistsException(AppException):
    message = "Object already exists"


class ObjectNotFoundException(AppException):
    message = "Object not found"


class MultipleObjectsFoundException(AppException):
    message = "Multiple objects found"


class ObjectInUseException(AppException):
    message = "Object in use"
