#!/usr/bin/python3

from semanticcad.csg.node import Node
from semanticcad.csg.operation import Operation
from semanticcad.csg.meshevaluator import MeshEvaluator

class Part:

    def __init__(self, root: Node):
        self.root = root

    def union(self, other):
        return Part(
            Node(Operation.UNION, self.root, other.root)
        )

    def difference(self, other):
        return Part(
            Node(Operation.DIFFERENCE, self.root, other.root)
        )

    def intersection(self, other):
        return Part(
            Node(Operation.INTERSECTION, self.root, other.root)
        )

    def translate(self, vector):
        return Part(
            Node(
                Operation.TRANSLATE,
                self.root,
                vector=vector,
            )
        )

    def rotate(self, axis, angle):
        return Part(
            Node(
                Operation.ROTATE,
                self.root,
                axis=axis,
                angle=angle,
            )
        )

    def mirror(self, normal):
        return Part(
            Node(
                Operation.MIRROR,
                self.root,
                normal=normal,
            )
        )
    
    '''
    def scale(self, factor):
        return Part(
            Node(
                Operation.SCALE,
                self.root,
                factor=factor,
            )
        )
    '''
    
    def __repr__(self):
        return f"Part(root={self.root!r})"
        
    @property
    def mesh(self):
        return MeshEvaluator.evaluate(self)

        
    def to_dot(self, filepath):
        """
        Exporta a árvore de operações em formato Graphviz (.dot).
        """

        lines = [
            "digraph Part {",
            '    rankdir=TB;',
            '    node [shape=box];',
        ]

        counter = [0]

        def visit(node):
            my_id = counter[0]
            counter[0] += 1

            if node.is_leaf:
                label = node.primitive.__class__.__name__
            else:
                label = node.operation.name

            lines.append(f'    node{my_id} [label="{label}"];')

            for child in node.children:
                child_id = visit(child)
                lines.append(f"    node{my_id} -> node{child_id};")

            return my_id

        visit(self.root)

        lines.append("}")

        with open(filepath, "w") as f:
            f.write("\n".join(lines))
