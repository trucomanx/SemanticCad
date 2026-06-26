#!/usr/bin/python3

from semanticcad.primitives.pribox import PriBox
from semanticcad.csg.node import Node
from semanticcad.csg.operation import Operation
from semanticcad.csg.part import Part


class Box(Part):

    def __init__(self, **kwargs):
        primitive = PriBox(**kwargs)

        super().__init__(
            Node(
                Operation.PRIMITIVE,
                primitive=primitive
            )
        )
