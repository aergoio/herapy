# -*- coding: utf-8 -*-

from google.protobuf.json_format import MessageToJson


class Peer:
    def __init__(self):
        self.__info = None
        self.__address = None
        self.__port = None
        self.__id = None
        self.__state = None

    @property
    def info(self):
        return MessageToJson(self.__info)

    @info.setter
    def info(self, v):
        self.__info = v
        self.__address = v.address
        self.__port = v.port
        self.__id = v.peerID

    @property
    def address(self):
        return self.__address

    @property
    def port(self):
        return self.__port

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, s):
        self.__state = s
