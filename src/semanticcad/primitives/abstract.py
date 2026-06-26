#!/usr/bin/python3

from abc import ABC, abstractmethod
from semanticcad.stl.generate import vertices_faces_to_binary_stl

class Primitive(ABC):


    def __init__(self):
        self._mesh = self._build_mesh()
        
    @abstractmethod
    def _build_mesh(self):
        """
        Retorna um dict contendo:

            {
                "vertices": np.ndarray,
                "face_indices": list[tuple[int, int, int]],
                "labels": list[str]
            }
        """
        pass

    @property
    def mesh(self):
        return self._mesh

    @property
    def vertices(self):
        return self._mesh.vertices

    @property
    def faces(self):
        return self._mesh.face_indices

    @property
    def labels(self):
        return self._mesh.labels

    def _repr_helper(self, *attrs):
        values = ", ".join(f"{a}={getattr(self, a)!r}" for a in attrs)
        return f"{self.__class__.__name__}({values})"

    def to_stl(self, filepath):
        vertices_faces_to_binary_stl(
            self.vertices,
            self.faces,
            filepath
        )
