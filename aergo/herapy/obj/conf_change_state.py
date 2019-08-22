# -*- coding: utf-8 -*-

import enum
import json

from google.protobuf.json_format import MessageToJson
from ..grpc.raft_pb2 import ConfChangeState


@enum.unique
class ChangeConfState(enum.Enum):
    """ ChangeConfState holds the state of the request 'changeCluster'
    to change configuration of RAFT cluster.
    """
    PROPOSED = ConfChangeState.Value("CONF_CHANGE_STATE_PROPOSED")
    SAVED = ConfChangeState.Value("CONF_CHANGE_STATE_SAVED")
    APPLIED = ConfChangeState.Value("CONF_CHANGE_STATE_APPLIED")


class ChangeConfInfo:
    """ ChangeConfInfo shows the state of the request 'changeCluster'
    to change configuration of RAFT cluster and member list of the cluster.
    """
    def __init__(self, state):
        self.__info = json.loads(MessageToJson(state))
        self.__state = ChangeConfState(state.State)
        self.__members = self.__info["Members"]

    def __str__(self):
        return json.dumps(self.json(), indent=2)

    def json(self):
        return self.__info

    @property
    def state(self):
        return self.__state

    @property
    def members(self):
        return self.__members
