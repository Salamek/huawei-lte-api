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


class ResponseErrorLoginCsrfException(ResponseErrorException):
    pass


class ResponseErrorWrongSessionToken(ResponseErrorException):
    pass


class LoginErrorInvalidCredentialsException(ResponseErrorException):
    """Base class for login errors caused by permanently invalid credentials."""


class LoginErrorUsernameWrongException(LoginErrorInvalidCredentialsException):
    pass


class LoginErrorPasswordWrongException(LoginErrorInvalidCredentialsException):
    pass


class LoginErrorAlreadyLoginException(ResponseErrorException):
    pass


class LoginErrorUsernamePasswordWrongException(LoginErrorInvalidCredentialsException):
    pass


class LoginErrorUsernamePasswordOverrunException(ResponseErrorException):
    pass


class LoginErrorUsernamePasswordModifyException(ResponseErrorException):
    pass


class RequestFormatException(ResponseErrorException):
    pass
