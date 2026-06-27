#!/usr/bin/python3

from semanticcad.csg.box      import Box
from semanticcad.csg.cylinder import Cylinder

# BOX
box = Box(l1=20, l2=30, l3=10)
print(box,"\n")


# CYLINDER
cyl = Cylinder(radius=5, height=20)
print(cyl,"\n")

# PART
piece = box.translate([10, 0, 0]).union(cyl.rotate([0, 1, 0], 90))
piece.to_dot("operations.dot")
print(piece,"\n")

# 
part1 = box.translate([5,0,0])
print(type(box)," --TRANSLATE--> ", type(part1))
print(part1, "\n")

'''
# falta implementar
# Mesh deve ter alias=["","",....,""] por falta

box = Box(l1=20, l2=30, l3=10, alias={"010": "Vertice1", "111": "Vertice2"})
box.
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
