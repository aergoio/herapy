from .exception import AergoException


class ConversionException(AergoException):
    def __init__(self, msg):
        self.error_msg = msg
        self.exception_type = AergoException.Conv

    def __str__(self):
        print_err = "{0}: {1}".format(self.exception_type, self.error_msg)

        return print_err
