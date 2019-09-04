# -*- coding: utf-8 -*-

import json

from google.protobuf.json_format import MessageToJson


class NameInfo():
    """ NameInfo is used to store information of name system."""
    def __init__(self, info):
        self.__info = json.loads(MessageToJson(info))
        self.__name = self.__info['name']['name']

    @property
    def info(self):
        return self.__info

    @property
    def name(self):
        return self.__name

    def json(self):
        rt = self.__info
        rt['name'] = self.name
        return rt

    def __str__(self):
        return json.dumps(self.json(), indent=2)
