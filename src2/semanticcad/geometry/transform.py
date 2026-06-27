# semanticcad/geometry/transform.py

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



