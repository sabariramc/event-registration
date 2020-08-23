#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 08-Jun-2020
"""


class HTTPException(Exception):

    def __init__(self, code, message, data):
        self.code = code
        self.data = data
        super().__init__(message)


class HTTPExceptionClientError(HTTPException):

    def __init__(self, code, message, data):
        super(HTTPExceptionClientError, self).__init__(code, message, data)


class HTTPExceptionBadRequest(HTTPExceptionClientError):

    def __init__(self, message, data=None):
        super(HTTPExceptionBadRequest, self).__init__(400, message, data)


class HTTPExceptionForbidden(HTTPExceptionClientError):

    def __init__(self, message, data=None):
        super(HTTPExceptionForbidden, self).__init__(403, message, data)


class HTTPExceptionNotFound(HTTPExceptionClientError):

    def __init__(self, message, data=None):
        super(HTTPExceptionNotFound, self).__init__(404, message, data)


class HTTPExceptionConflict(HTTPExceptionClientError):

    def __init__(self, message=None, data=None):
        super(HTTPExceptionConflict, self).__init__(409, message, data)


class HTTPExceptionServerError(HTTPException):
    def __init__(self, message, data):
        super(HTTPExceptionServerError, self).__init__(550, message, data)

# if __name__ == "__main__":
#     obj = KNOBException("hello")
#     print str(obj)
