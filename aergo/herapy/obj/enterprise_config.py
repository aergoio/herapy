# -*- coding: utf-8 -*-

import copy
import json

from google.protobuf.json_format import MessageToJson


class EnterpriseConfig:
    """ EnterpriseConfig stores the result of GetEnterpriseConfig. """
    def __init__(self, config):
        self.__json = json.loads(MessageToJson(config))
        self.__key = self.__json.get('key', None)
        self.__on = self.__json.get('on', False)
        self.__values = self.__json.get("values", [])

    def __str__(self):
        return json.dumps(self.json(), indent=2)

    def json(self):
        return copy.deepcopy(self.__json)

    @property
    def key(self):
        return self.__key

    @property
    def on(self):
        return self.__on

    @property
    def values(self):
        return self.__values
