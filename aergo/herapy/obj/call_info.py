# -*- coding: utf-8 -*-

import json

class CallInfo():
    """ CallInfo is used to store contract call/query arguments for json serialization."""
    def __init__(self, name, args):
        self.Name = name
        self.Args = args
