class AppException(Exception):
    message = "Неожиданная ошибка"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class ObjectAlreadyExistsException(AppException):
    message = "Объект уже существует"


class ObjectNotFoundException(AppException):
    message = "Объект не найден"
