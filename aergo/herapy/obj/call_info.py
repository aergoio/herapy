# -*- coding: utf-8 -*-


class CallInfo():
    """ CallInfo is used to store contract call/query arguments for json serialization."""
    def __init__(self, name, args):
        self.name = name
        self.args = args
