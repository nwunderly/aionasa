
"""
aio-nasa exceptions
"""


class NASAException(Exception):
    pass


class APIException(NASAException):
    def __init__(self, code, reason):
        self.code = code
        self.reason = reason
        super().__init__(f"{code} - {reason}")


class ArgumentError(NASAException):
    pass


class PandasNotFound(NASAException):
    pass


# class NotFound(APIException):
#     pass
#
#
# class TooManyRequests(APIException):
#     pass
