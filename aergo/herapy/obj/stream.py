# -*- coding: utf-8 -*-

import grpc
import grpc._channel


class Stream:
    def __init__(self, grpc_stream):
        self._grpc_stream = grpc_stream

        self.__started = False
        self.__stopped = False

    def start(self):
        self.__started = True
        self.__stopped = False

    def stop(self):
        self.__started = False
        self.__stopped = True

    @property
    def started(self):
        return self.__started

    @property
    def stopped(self):
        return self.__stopped

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next()
        except grpc._channel._Rendezvous:
            raise RuntimeError("stream is cancelled")

    def next(self):
        # need to implement for each subclass
        pass

    def cancel(self):
        self._grpc_stream.cancel()

    def cancelled(self):
        return self._grpc_stream.cancelled()

    def done(self):
        return self._grpc_stream.done()

    def is_active(self):
        return self._grpc_stream.is_active()

    def running(self):
        return self._grpc_stream.running()

    """
    def result(self, timeout):
        try:
            result = self._grpc_stream.result(timeout)
        except grpc.FutureTimeoutError:
            raise TimeoutError
        return result

    def add_callback(self, fn):
        result = self._grpc_stream.add_callback(fn)
        return result
        
    def exception(self, timeout):
        try:
            result = self._grpc_stream.exception(timeout)
        except grpc.FutureTimeoutError:
            raise TimeoutError
        return result
        
    def time_remaining(self):
        result = self._grpc_stream.time_remaining()
        return result
    """
