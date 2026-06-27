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
