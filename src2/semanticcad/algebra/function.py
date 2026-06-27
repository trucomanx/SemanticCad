#!/usr/bin/python3

import numpy as np

def normalize(v):
    v = np.asarray(v, dtype=float)

    s = np.max(np.abs(v))
    if s == 0:
        raise ValueError("Vetor nulo.")

    v = v / s
    return v / np.linalg.norm(v)
