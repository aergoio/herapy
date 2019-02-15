# -*- coding: utf-8 -*-

"""Enumeration of Smart contract Status."""

import enum


@enum.unique
class SmartcontractStatus(enum.Enum):
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
