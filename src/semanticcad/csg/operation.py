#!/usr/bin/python3

from enum import Enum, auto


class Operation(Enum):
    PRIMITIVE = auto()

    UNION = auto()
    DIFFERENCE = auto()
    INTERSECTION = auto()

    TRANSLATE = auto()
    ROTATE = auto()
    MIRROR = auto()
    #SCALE = auto()
