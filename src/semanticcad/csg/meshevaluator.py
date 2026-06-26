#!/usr/bin/python3

import numpy as np

from semanticcad.geometry.mesh      import Mesh
from semanticcad.csg.operation      import Operation
from semanticcad.geometry.transform import transform

class MeshEvaluator:

    @staticmethod
    def evaluate(part):
        return MeshEvaluator._evaluate_node(part.root)

    @staticmethod
    def _evaluate_node(node):

        # -----------------------------
        # folha
        # -----------------------------
        if node.operation == Operation.PRIMITIVE:
            return node.primitive.mesh.copy()

        # -----------------------------
        # translate
        # -----------------------------
        elif node.operation == Operation.TRANSLATE:

            mesh = MeshEvaluator._evaluate_node(node.children[0])

            return transform(mesh, node)

        # -----------------------------
        # rotate
        # -----------------------------
        elif node.operation == Operation.ROTATE:
            raise NotImplementedError("ROTATE")

        # -----------------------------
        # mirror
        # -----------------------------
        elif node.operation == Operation.MIRROR:
            raise NotImplementedError("MIRROR")

        # -----------------------------
        # union
        # -----------------------------
        elif node.operation == Operation.UNION:
            raise NotImplementedError("UNION")

        # -----------------------------
        # difference
        # -----------------------------
        elif node.operation == Operation.DIFFERENCE:
            raise NotImplementedError("DIFFERENCE")

        # -----------------------------
        # intersection
        # -----------------------------
        elif node.operation == Operation.INTERSECTION:
            raise NotImplementedError("INTERSECTION")

        raise RuntimeError(f"Operação desconhecida: {node.operation}")
