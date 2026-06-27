#!/usr/bin/python3

from semanticcad.primitives.pricylinder import PriCylinder
from semanticcad.primitives.pribox      import PriBox

box = PriBox(l1=1.0, l2=2.0, l3=3.0)
box.to_stl("teste_box.stl")
print(box)

cyl = PriCylinder(radius=1.0, height=1.0, circle_steps=100)
cyl.to_stl("teste_cylinder.stl")
print(cyl)
