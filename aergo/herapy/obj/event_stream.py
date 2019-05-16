# -*- coding: utf-8 -*-

from .stream import Stream
from .event import Event


class EventStream(Stream):
    def __init__(self, event_stream):
        super().__init__(event_stream)

    def next(self):
        return Event(grpc_event=next(self._grpc_stream))
