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

