import numpy as np
from semanticcad.algebra.function import normalize


class Frame3D:
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
        
if __name__ == "__main__":

    frame = Frame3D(   origin=[0, 0, 0],
                       v1=[1, 0, 0],
                       v2=[0, 1, 0]  )
    
    print(frame)
