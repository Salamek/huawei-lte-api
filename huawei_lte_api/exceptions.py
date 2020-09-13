class ResponseErrorException(Exception):
    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.code = code


class ResponseErrorNotSupportedException(ResponseErrorException):
    pass


class ResponseErrorLoginRequiredException(ResponseErrorException):
    pass


class ResponseErrorSystemBusyException(ResponseErrorException):
    pass


class ResponseErrorLoginCsfrException(ResponseErrorException):
    """Deprecated misspelling, use ResponseErrorLoginCsrfException instead."""


class ResponseErrorLoginCsrfException(ResponseErrorLoginCsfrException):
    pass


class LoginErrorUsernameWrongException(ResponseErrorException):
    pass


class LoginErrorPasswordWrongException(ResponseErrorException):
    pass


class LoginErrorAlreadyLoginException(ResponseErrorException):
    pass


class LoginErrorUsernamePasswordWrongException(ResponseErrorException):
    pass


class LoginErrorUsernamePasswordOverrunException(ResponseErrorException):
    pass


class LoginErrorUsernamePasswordModifyException(ResponseErrorException):
    pass
