# -*- coding: utf-8 -*-


class ResourceUnavailable(Exception):
    """Exception representing a failed request to a resource"""

    def __init__(self, msg, http_response):
        Exception.__init__(self)
        self._msg = msg
        self._status = http_response.status_code

    def __str__(self):
        return "{} (HTTP status: {})".format(self._msg, self._status)


class Unauthorized(ResourceUnavailable):
    pass


class MissingOrInvalidParameter(ResourceUnavailable):
    pass


class NoPermission(ResourceUnavailable):
    pass


class NotFound(ResourceUnavailable):
    pass


class TokenError(Exception):
    pass


class GenericException(Exception):
    """Exception representing a failed request to a resource"""

    def __init__(self, msg, input):
        Exception.__init__(self)
        self._msg = msg
        self._input = input

    def __str__(self):
        return "{} (Input: {})".format(self._msg, self._input)


class DoesNotExist(GenericException):
    pass
