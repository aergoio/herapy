# -*- coding: utf-8 -*-

import copy
import json

from google.protobuf.json_format import MessageToJson


class Abi():
    """ NameInfo is used to store information of name system."""
    def __init__(self, abi):
        self.__json = json.loads(MessageToJson(abi))
        self.__version = self.__json['version']
        self.__language = self.__json['language']
        self.__functions = self.__json['functions']
        self.__state_variables = self.__json['stateVariables']

    @property
    def version(self):
        return self.__version

    @property
    def language(self):
        return self.__language

    @property
    def functions(self):
        return self.__functions

    @property
    def state_variables(self):
        return self.__state_variables

    def json(self):
        return copy.deepcopy(self.__json)

    def __str__(self):
        return json.dumps(self.json(), indent=2)
