# -*- coding: utf-8 -*-

"""Enumeration of Smart contract Status."""

import enum


@enum.unique
class TxResultStatus(enum.Enum):
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
