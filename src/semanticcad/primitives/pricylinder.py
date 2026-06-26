import numpy as np
from semanticcad.geometry.axes import Frame3D
from semanticcad.geometry.mesh import Mesh
from semanticcad.primitives.abstract import Primitive

class PriCylinder(Primitive):
    def __init__(self, radius=1.0, height=1.0, circle_steps=100):
        self.frame = Frame3D.Canonical

        self.radius = float(radius)
        self.height = float(height)
        self.circle_steps = int(circle_steps)

        super().__init__()

    def _circle_point(self, angle, center, radius_vec1, radius_vec2):
        return (
            center
            + np.cos(angle) * radius_vec1
            + np.sin(angle) * radius_vec2
        )

    def _build_mesh(self):
        f = self.frame
        o = f.origin

        # eixo do cilindro
        axis = f.e3 * self.height

        # base plane
        r1 = f.e1 * self.radius
        r2 = f.e2 * self.radius

        cb = o 
        ct = o + axis 

        V = []
        F = []
        LABELS = []

        # centers
        cb_index = 0
        ct_index = 1

        V.append(cb)  # cb
        V.append(ct)  # ct

        LABELS.append("cb")
        LABELS.append("ct")

        n = self.circle_steps

        bottom = []
        top = []

        # vertices do círculo
        for i in range(n):
            a = 2 * np.pi * i / n

            b = self._circle_point(a, cb, r1, r2)
            t = self._circle_point(a, ct, r1, r2)

            bi = len(V)
            V.append(b)
            LABELS.append(f"b{i}")

            ti = len(V)
            V.append(t)
            LABELS.append(f"t{i}")

            bottom.append(bi)
            top.append(ti)

        # faces laterais
        for i in range(n):
            i2 = (i + 1) % n

            b0 = bottom[i]
            b1 = bottom[i2]
            t0 = top[i]
            t1 = top[i2]

            # dois triângulos por quad lateral
            F.append((b0, b1, t1))
            F.append((b0, t1, t0))

        # tampa inferior
        for i in range(1, n - 1):
            F.append((bottom[0], bottom[i], bottom[i + 1]))

        # tampa superior
        for i in range(1, n - 1):
            F.append((top[0], top[i + 1], top[i]))

        return Mesh(np.array(V), F, LABELS)


    def __repr__(self):
        return self._repr_helper("radius", "height", "circle_steps")
        
if __name__ == "__main__":
    pri = PriCylinder(radius=1.0, height=1.0, circle_steps=100)
    pri.to_stl("teste_cylinder.stl")
    
    print(pri)
    print(pri.mesh)
