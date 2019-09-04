# -*- coding: utf-8 -*-

import json

from google.protobuf.json_format import MessageToJson

from .address import Address

class NameInfo():
    """ NameInfo is used to store information of name system."""
    def __init__(self, info):
        self.__info = json.loads(MessageToJson(info))
        self.__name = info.name.name
        self.__owner = Address.encode(info.owner)
        self.__dest = Address.encode(info.destination)

    @property
    def info(self):
        return self.__info

    @property
    def name(self):
        return self.__name

    @property
    def owner(self):
        return self.__owner

    @property
    def destination(self):
        return self.__dest

    def json(self):
        return {
            'name': self.name,
            'owner': self.owner,
            'destination': self.destination
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)
