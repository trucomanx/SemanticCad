# semanticcad/geometry/transform.py

import numpy as np

def rotate_mesh(V, axis, angle):
    axis = axis / np.linalg.norm(axis)
    angle = np.deg2rad(angle)

    # Rodrigues rotation formula
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])

    R = (
        np.eye(3)
        + np.sin(angle) * K
        + (1 - np.cos(angle)) * (K @ K)
    )

    return V @ R.T
    
def mirror_mesh(V, normal):
    normal = normal / np.linalg.norm(normal)
    return V - 2 * (V @ normal)[:, None] * normal

def transform(mesh, node):
    """
    Aplica transformações em uma malha (V, F).
    Retorna nova Mesh (NÃO muta original).
    """

    V = mesh.vertices.copy()

    op = node.operation

    # -----------------------
    # TRANSLATE
    # -----------------------
    if op.name == "TRANSLATE":
        v = np.asarray(node.params["vector"], dtype=float)
        V = V + v

    # -----------------------
    # ROTATE (placeholder)
    # -----------------------
    elif op.name == "ROTATE":
        axis = np.asarray(node.params["axis"], dtype=float)
        angle = node.params["angle"]

        V = rotate_mesh(V, axis, angle)

    # -----------------------
    # MIRROR (placeholder)
    # -----------------------
    elif op.name == "MIRROR":
        normal = np.asarray(node.params["normal"], dtype=float)

        V = mirror_mesh(V, normal)

    else:
        raise ValueError(f"Transform não suportada: {op}")

    return mesh.__class__(V, mesh.face_indices, mesh.labels)
    
