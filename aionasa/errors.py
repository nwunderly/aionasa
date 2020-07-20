
"""
aio-nasa exceptions
"""


class NASAException(Exception):
    pass


class APIException(NASAException):
    pass


class ArgumentError(NASAException):
    pass

