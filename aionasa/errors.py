
"""
aio-nasa exceptions
"""


class NASAException(Exception):
    pass


class APIException(NASAException):
    pass


class ArgumentError(NASAException):
    pass


class PandasNotFound(NASAException):
    pass

