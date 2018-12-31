# -*- coding: utf-8 -*-

"""Enumeration of Smart contract Status."""

import enum


@enum.unique
class PeerStatus(enum.Enum):
    """
    github.com/aergoio/aergo/types/peerstate.go
    """
    STARTING = 0
    HANDSHAKING = 1
    RUNNING = 2
    DOWN = 3
    STOPPED = 4
