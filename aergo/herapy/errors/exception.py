# -*- coding: utf-8 -*-


class AergoException(Exception):
    Comm = "Communication Exception"

    """
    def __init__(self, msg, code, details):
        self.__message = msg
        self.__error_code = code
        self.__error_details = details

    def __str__(self):
        print_err = "{0} ({1}): {2}".format(self.__message, self.__error_code, self.__error_details)

        return print_err
    """
    def __init__(self, e, exception_type):
        self.__error_code = e.code()
        self.__error_details = e.details()
        self.__exception_type = exception_type

    def __str__(self):
        print_err = "{0} ({1}): {2}".format(self.__exception_type, self.__error_code, self.__error_details)
        return print_err


class CommunicationException(AergoException):
    def __init__(self, exception_type):
        super().__init__(exception_type, AergoException.Comm)
