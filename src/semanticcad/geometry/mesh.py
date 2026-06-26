#!/usr/bin/python3

class Mesh:
    def __init__(self, vertices, face_indices, labels):
        self.vertices = vertices
        self.face_indices = face_indices
        self.labels = labels

    def __repr__(self):
        return (
            f"Mesh("
            f"vertices={self.vertices!r}, "
            f"face_indices={self.face_indices!r}, "
            f"labels={self.labels!r})"
        )
        
    def copy(self):
        return Mesh(
            self.vertices.copy(),
            self.face_indices.copy(),
            self.labels.copy()
        )
