class ResponseErrorException(Exception):
    pass


class ResponseErrorNotSupportedException(ResponseErrorException):
    pass


class ResponseErrorLoginRequiredException(ResponseErrorException):
    pass


class ResponseErrorSystemBusyException(ResponseErrorException):
    pass


class ResponseErrorLoginCsfrException(ResponseErrorException):
    pass