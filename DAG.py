from DAGNode import DAGNode


class DAG:
    """
        Class representing a DAG search structure with a reference
        to the root node
    """

    def __init__(self, root):
        assert isinstance(root, DAGNode)
        self.root = root
