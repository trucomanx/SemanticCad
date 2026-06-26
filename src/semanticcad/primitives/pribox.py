import numpy as np
from semanticcad.geometry.axes import Frame3D
from semanticcad.geometry.mesh import Mesh
from semanticcad.primitives.abstract import Primitive

class PriBox(Primitive):
    def __init__(self, l1=1.0, l2=1.0, l3=1.0):
        self.frame = Frame3D.Canonical

        self.l1 = float(l1)
        self.l2 = float(l2)
        self.l3 = float(l3)
        
        super().__init__()

    def _build_mesh(self):
        f = self.frame
        o = f.origin

        e1 = f.e1 * self.l1
        e2 = f.e2 * self.l2
        e3 = f.e3 * self.l3

        V = np.array([
            o,
            o + e1,
            o + e1 + e2,
            o + e2,

            o + e3,
            o + e3 + e1,
            o + e3 + e1 + e2,
            o + e3 + e2,
        ])
        
        F = [(0, 1, 2), (0, 2, 3),
             (4, 6, 5), (4, 7, 6),
             (0, 5, 1), (0, 4, 5),
             (1, 6, 2), (1, 5, 6),
             (2, 7, 3), (2, 6, 7),
             (3, 4, 0), (3, 7, 4) ]
        LABELS = ["000","010","110","100","001","011","111","101"]

        return Mesh(V, F, LABELS)

    def __repr__(self):
        return self._repr_helper("l1", "l2", "l3")


if __name__ == "__main__":

    pri = PriBox(l1=1.0, l2=2.0, l3=3.0)
    pri.to_stl("teste_box.stl")
    
    print(pri)
    print(pri.mesh)
