# -*- coding: utf-8 -*-

import json

from google.protobuf.json_format import MessageToJson


class NameInfo():
    """ NameInfo is used to store information of name system."""
    def __init__(self, info):
        self.__info = json.loads(MessageToJson(info))

    def json(self):
        return self.__info

    def __str__(self):
        return json.dumps(self.json(), indent=2)
