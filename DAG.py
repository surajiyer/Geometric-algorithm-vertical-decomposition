from DAGNode import DAGNode
import pprint as pp


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

    def __repr__(self):
        return '<DAG>\n\t' + pp.pformat(list(self.in_order(self.root)), indent=4) + '\n</DAG>'
        # return '<DAG: \n%s>' % '\n\n'.join(str(n) for n in list(self.in_order(self.root)))
