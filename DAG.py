from DAGNode import DAGNode


class DAG:
    """
    Class representing a DAG search structure with a reference
    to the root node
    """

    def __init__(self, root):
        assert isinstance(root, DAGNode)
        self.root = root

    def in_order(self, node):
        if node:
            yield from self.in_order(node.left_child)
            yield node
            yield from self.in_order(node.right_child)
