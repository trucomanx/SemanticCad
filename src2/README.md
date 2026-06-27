# SemanticCad

# Project Description
I am designing a Python library called SemanticCAD.

SemanticCAD is a computational geometry and design library for mechanical parts based on mesh representations enriched with structured semantic metadata.

The goal of SemanticCAD is to provide a single-source-of-truth model for mechanical design, where geometry, semantic meaning, and engineering documentation are defined in the same system and consistently propagated through geometric transformations.

Unlike traditional CAD systems that separate modeling, annotation, and technical drawing generation into different tools or manual workflows, SemanticCAD generates all representations from a unified semantic model.

The library is designed to:

- represent mechanical parts as meshes enriched with topology-aware semantic information
- support parametric and constructive geometry operations (translate, rotate, union, difference)
- preserve semantic consistency through all transformations
- enable vertex-level semantic labeling through two distinct concepts:
  - primitive labels (structural, class-level identifiers)
  - user-defined aliases (instance-level semantic naming)
- support engineering dimensions as explicit relationships between vertices
- generate multiple outputs from the same model, including STL files and technical drawings

SemanticCAD is intended as both:
- a modeling system
- and a semantic compilation framework for mechanical design

# Technical Description

SemanticCAD is a library for describing mechanical parts using parametric-geometric modeling based on meshes enriched with semantic metadata.

Model:
Geometry (Mesh)
Topology (Primitive Labels)
Semantics (User Aliases + Engineering Dimensions)

Model: Mesh + Semantic Metadata = Part
Process: Mesh -> Mesh transformation -> New Part

Mesh transformation
- Geometric update
- Semantic propagation (aliases + dimensions)

All transformations (translate, rotate, union, difference) produce a new Part. Geometry is recomputed. Semantic metadata is propagated based on topological correspondence.

Vertex aliases are attached to mesh topology (vertex identity), not geometric coordinates. They are preserved through transformations.

Vertex aliases are defined by the primitive topology. Each primitive defines a fixed set of named vertices. These names are preserved through geometric transformations.

Cylinder primitives define a deterministic labeled topology including axial and discretized perimeter vertices. These labels depend on primitive parameters (e.g., radial_segments) and remain stable under transformations.

All primitives are created oriented in their canonical form (Frame3D), with origin in `[0,0,0]` and axes `[[0,0,0],[0,1,0],[0,0,1]]`.

Each primitive defines a fixed set of topological vertex labels. Labels are intrinsic, immutable, and shared across all instances of the same primitive type.

Vertex aliases are user-defined names bound to primitive labels within a Part instance. Aliases are local, optional, and do not modify the underlying topology.

Analogy:
A primitive is like the concept of a human body (class), where "right arm" and "left arm" are structural labels shared by all humans.
An instance (e.g., a specific person like "Fernando") can assign personal names (aliases) to these structural parts, such as calling the right arm "brazoA0".

Engineering dimensions are explicit semantic relations between two vertices within a Part, representing Euclidean distance in 3D space.

Semantic metadata operates on top of topology:
- Labels define geometric identity
- Aliases define user interpretation of labels
- Dimensions define relations between labels


Part (Single Source of Truth)

```
├── Mesh (geometry)
├── Primitive Labels (topological identity)
├── Vertex Aliases (user-defined naming of labels)
├── Engineering Dimensions (relations between labels)
├── Documentation Levels
└── ...
```

A Part consists of a mesh and semantic metadata that survive geometric transformations and are used to generate multiple representations such as STL and technical drawings.

Unlike traditional CAD systems, SemanticCAD models not only the geometry of a part but also its semantic information: vertex aliases, engineering dimensions, documentation levels, and other metadata that express the designer's intent.

From a single semantic description, multiple artifacts can be consistently generated:
- STL meshes
- Technical drawings
- Future manufacturing formats

# Architecture Choice:
I prefer an object-oriented design with an abstract base class Part that encapsulates:

The mesh geometry, and
All associated semantic information (primitive labels, user aliases, engineering dimensions, etc.).

Concrete primitives such as Box and Cylinder inherit from Part. Each subclass is responsible for:

Generating its own mesh in the constructor via a dedicated method (_generate_mesh()), and
Defining its internal topological labels (a fixed naming convention for important vertices).

These primitive labels act as stable internal identifiers. They serve as a bridge so that user-defined aliases can be correctly mapped to the corresponding vertices in the mesh. This way, semantic information remains consistent even after geometric transformations.

In SemanticCAD, geometric operations such as union, difference, intersection, and translate are primarily exposed as top-level functions for a cleaner and more intuitive user experience (e.g., sc.union(part1, part2)). This design prioritizes readability and follows a functional approach for combining parts. For convenience and object-oriented fluency, these operations are also available as methods on the Part class (e.g., part1.union(part2)), which internally delegate to the standalone functions. This dual interface allows users to choose the style that best fits their workflow while maintaining consistency across the library.


Geometric operations such as union, difference, and intersection are implemented as standalone functions in geometry/boolean.py, while transformations like translate and rotate are available both as methods on Part and in geometry/transform.py

# Proposed library usage (IMPORTANT!!!!)

This is an example usage of the proposed library.


```python

import semanticcad as sc


box1 = sc.Box(l1=20, l2=30, l3=10, alias_map={"010": "Vertice1", "001": "Vertice2"})
cyl1 = sc.Cylinder(h=10, r=2, radial_segments=100, alias_map={"c0_bottom": "CentroAbaixo",
                                                              "c0_top": "CentroAcima", 
                                                              "b0": "VerticePerimetroAbaixoStep0", 
                                                              "t1": "VerticePerimetroAcimaStep1"})

box2 = box1.translate([10,10,0]) # box2 have the same aliases of box1

# aliast_priority=0 gives priority to aliases of Box1, eliminates repeated aliases, alias are uniques!
part1 = sc.union(box1,box2, alias_priority=0) 
part2 = box1.union(box2) # alias_priority to box1
part3 = box2.union(box1) # alias_priority to box2

print(part1.vertex_aliases()) # {"Vertice1": [0,30,0], "Vertice2": 0,0,10}
print(part1.vertex("Vertice2")) # [0,0,10]
print(part1.vertex("Vertice1")) # [0,30,0]
print(part1.vertex(0))          # [0,0,0]
print(part1._vertex_with_alias("Vertice1")) # [0,30,0] # this method will not be exposed
print(part1._vertex_with_index(0))          # [0,0,0]  # this method will not be exposed

#will always be a Euclidean distance between two points
part1.add_dimension("Vertice1", # part1._vertex_with_alias("Vertice1")
                    0,          # part1._vertex_with_index(0)
                    "D1", #label
                    level=0#level
                )

part1.add_dimension(0,          # part1._vertex_with_index(0)
                    "Vertice2", # part1._vertex_with_alias("Vertice2")
                    "D2", #label
                    level=0#level
                )
                
part1.export_techdraw("filename.pdf",level=[0])
part1.export_stl("filename.stl") # binary

```
  
  
# Current files  

'semanticcad/__init__.py'

```
from .primitives.box import Box
from .primitives.cylinder import Cylinder

# Para facilitar ainda mais o uso:
__all__ = ['Box', 'Cylinder']

```

'semanticcad/export/stl.py'

```python
import numpy as np
from stl import mesh
# pip install numpy
# pip install numpy-stl


def vertices_faces_to_binary_stl(V, F, filepath):
    triangles = np.zeros(len(F), dtype=mesh.Mesh.dtype)
    m = mesh.Mesh(triangles)

    for i, (a, b, c) in enumerate(F):
        m.vectors[i] = np.array([
            V[a],
            V[b],
            V[c],
        ])

    m.save(filepath)


if __name__ == "__main__":

    # 8 vértices de uma caixa
    V = [
        [0, 0, 0],  # 0
        [1, 0, 0],  # 1
        [1, 1, 0],  # 2
        [0, 1, 0],  # 3

        [0, 0, 1],  # 4
        [1, 0, 1],  # 5
        [1, 1, 1],  # 6
        [0, 1, 1],  # 7
    ]

    # 12 triângulos (2 por face)
    F = [
        # bottom (z=0)
        (0, 1, 2), (0, 2, 3),
        # top (z=1)
        (4, 6, 5), (4, 7, 6),
        # front (y=0)
        (0, 5, 1), (0, 4, 5),
        # back (y=1)
        (3, 2, 6), (3, 6, 7),
        # left (x=0)
        (0, 3, 7), (0, 7, 4),
        # right (x=1)
        (1, 5, 6), #(1, 6, 2),
    ]

    vertices_faces_to_binary_stl(V, F, "box.stl")
```  'semanticcad/geometry/axes.py'
 ```python  
import numpy as np
from semanticcad.algebra.function import normalize


class Frame3D:
    Canonical = None
    
    def __init__(self, origin=[0, 0, 0], v1=[1, 0, 0], v2=[0, 1, 0]):

        self.origin = np.asarray(origin, dtype=float)

        v1 = np.asarray(v1, dtype=float)
        v2 = np.asarray(v2, dtype=float)

        # eixo principal
        self.e1 = normalize(v1)

        # normal do plano (define "para cima" do frame)
        self.e3 = normalize(np.cross(self.e1, v2))

        # fecha base ortonormal
        self.e2 = normalize(np.cross(self.e3, self.e1))


    def __repr__(self):
        return (
            f"Frame3D(origin={self.origin}, "
            f"e1={self.e1}, e2={self.e2}, e3={self.e3})"
        )

Frame3D.Canonical = Frame3D(
    origin=[0, 0, 0],
    v1=[1, 0, 0],
    v2=[0, 1, 0]
)

if __name__ == "__main__":

    frame = Frame3D(   origin=[0, 0, 0],
                       v1=[1, 0, 0],
                       v2=[0, 1, 0]  )
    
    print(frame)  

```  
  
'semanticcad/core/mesh.py'

```python  
#!/usr/bin/python3

class Mesh:
    def __init__(self, vertices, face_indices, aliases):
        self.vertices = vertices
        self.face_indices = face_indices
        self.aliases = aliases

    def __repr__(self):
        return (
            f"Mesh("
            f"vertices={self.vertices!r}, "
            f"face_indices={self.face_indices!r}, "
            f"aliases={self.aliases!r})"
        )
        
    def copy(self):
        return Mesh(
            self.vertices.copy(),
            self.face_indices.copy(),
            self.aliases.copy()
        )
```  
  

`semanticcad/geometry/transform.py`

```python
import numpy as np

def mirror_mesh(V, normal):
    normal = np.asarray(normal, dtype=float)
    normal = normal / np.linalg.norm(normal)
    return V - 2 * np.outer(V @ normal, normal)

def translate_mesh(V, vector):
    """V: np.array (N, 3)"""
    return V + np.asarray(vector, dtype=float)   # ← Error corregido


def rotate_mesh(V, axis, angle_deg):
    """Rotación usando Rodrigues"""
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    angle = np.deg2rad(angle_deg)
    
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    
    R = (np.eye(3) +
         np.sin(angle) * K +
         (1 - np.cos(angle)) * (K @ K))
    
    return V @ R.T
```

`semanticcad/algebra/function.py`

```python
import numpy as np

def normalize(v):
    v = np.asarray(v, dtype=float)

    s = np.max(np.abs(v))
    if s == 0:
        raise ValueError("Vetor nulo.")

    v = v / s
    return v / np.linalg.norm(v)
```
