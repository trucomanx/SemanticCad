#!/usr/bin/python3

from semanticcad.primitives.pricylinder import PriCylinder
from semanticcad.primitives.pribox      import PriBox

box = PriBox(l1=1.0, l2=2.0, l3=3.0)
box.to_stl("teste_box.stl")

cyl = PriCylinder(radius=1.0, height=1.0, circle_steps=100)
cyl.to_stl("teste_cylinder.stl")

print(box)
print(cyl)

from semanticcad.csg.box      import Box
from semanticcad.csg.cylinder import Cylinder

box = Box(l1=20, l2=30, l3=10)

cyl = Cylinder(radius=5, height=20)

piece = (
    box
    .translate([10, 0, 0])
    .union(cyl.rotate([0, 1, 0], 90))
)

print(piece)

piece.to_dot("operations.dot")


part1 = box.translate([0,0,0])
print(type(box))
print(type(part1))
'''
# falta implementar
# Mesh deve ter alias=["","",....,""] por falta

box = Box(l1=20, l2=30, l3=10, alias={"010": "Vertice1", "111": "Vertice2"})
part1 = box.translate([0,0,0])

part1.add_legnth(   part1.vertice_with_alias(Vertice1),
                    part1.vertice_with_index(2),
                    "D1", #label
                    0#lelvel
                )
'''

print(box.mesh)
print(part1.mesh)
part1.to_stl("teste_box2.stl")
