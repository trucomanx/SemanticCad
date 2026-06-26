#!/usr/bin/python3

from semanticcad.primitives.pricylinder import PriCylinder
from semanticcad.csg.node import Node
from semanticcad.csg.operation import Operation
from semanticcad.csg.part import Part


class Cylinder(Part):

    def __init__(self, **kwargs):
        primitive = PriCylinder(**kwargs)

        super().__init__(
            Node(
                Operation.PRIMITIVE,
                primitive=primitive
            )
        )
