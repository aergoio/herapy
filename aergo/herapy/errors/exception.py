# -*- coding: utf-8 -*-


class AergoException(Exception):
    # Exception types
    Comm = "Communication Exception"

    def __init__(self, error, exception_type):
        self.__error = error
        self.__exception_type = exception_type

    def __str__(self):
        print_err = "{0} : {1}".format(self.__exception_type, self.__error)

        return print_err


class CommunicationException(AergoException):
    def __init__(self, error):
        self.__error_code = error.code()
        self.__error_details = error.details()
        self.__exception_type = AergoException.Comm

    def __str__(self):
        print_err = "{0} ({1}): {2}".format(self.__exception_type, self.__error_code, self.__error_details)

        return print_err


"""
Use this code when you add another module's exception.
You can see AergoException's print(__str__) format by using only this code.
If you want another format make __str__ like CommunicationException.

class TestException(AergoException):
    def __init__(self, error):
        super().__init__(error, EXCEPTION_TYPE)

"""
