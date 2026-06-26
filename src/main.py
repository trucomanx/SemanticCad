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


box2 = box.translate([5,0,0])

print(box.mesh.vertices)
print(box2.mesh.vertices)
