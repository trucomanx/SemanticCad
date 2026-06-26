#!/usr/bin/python3

from semanticcad.csg.operation import Operation

class Node:
    def __init__(self, operation, *children, primitive=None, **params):
        self.operation = operation
        self.children = list(children)
        self.primitive = primitive
        self.params = params

        if operation == Operation.PRIMITIVE:
            if primitive is None:
                raise ValueError("Primitive node requires a primitive.")
        else:
            if primitive is not None:
                raise ValueError("Only PRIMITIVE nodes may store a primitive.")

    def __repr__(self):
        return (
            f"Node("
            f"operation={self.operation.name}, "
            f"children={len(self.children)}, "
            f"params={self.params})"
        )
        
    def is_leaf(self):
        return self.operation == Operation.PRIMITIVE
        
    @property
    def arity(self):
        return len(self.children)
