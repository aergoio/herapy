# -*- coding: utf-8 -*-

import json

from google.protobuf.json_format import MessageToJson

from ..utils.encoding import encode_address


class NameInfo():
    """ NameInfo is used to store information of name system."""
    def __init__(self, info):
        self.__info = json.loads(MessageToJson(info))
        self.__name = info.name.name
        self.__owner = info.owner
        self.__dest = info.destination

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
        if self.owner is not None:
            owner = encode_address(self.owner)
        else:
            owner = ""

        if self.destination is not None:
            dest = encode_address(self.destination)
        else:
            dest = ""

        return {
            'name': self.name,
            'owner': owner,
            'destination': dest
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)
