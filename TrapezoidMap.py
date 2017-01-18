from Trapezoid import Trapezoid
from DAG import DAG
# from llist import dllist
import networkx as nx
import matplotlib.pyplot as plt
from MatPlotAnnotater import MatPlotAnnotater


class TrapezoidMap:
    """
    Class representing a trapezoidal map with a set of trapezoids
    """

    def __init__(self, trapezoids):
        assert isinstance(trapezoids, list) and all(isinstance(n, Trapezoid) for n in trapezoids)
        self.trapezoids = trapezoids
        # self.trapezoids = dllist(trapezoids)
        self.G = None

    def addTrapezoid(self, trapezoids):
        assert isinstance(trapezoids, list) and all(isinstance(t, Trapezoid) for t in trapezoids)
        self.trapezoids.extend(trapezoids)
        # self.trapezoids.extendright(trapezoids)

    def deleteTrapezoidFromMap(self, trapezoids):
        assert isinstance(trapezoids, list) and all(isinstance(t, Trapezoid) for t in trapezoids)
        self.trapezoids = [t for t in self.trapezoids if t not in trapezoids]
        for t in trapezoids:
            try:
                for n in t.left_neighbors:
                    n.right_neighbors.discard(t)
                for n in t.right_neighbors:
                    n.left_neighbors.discard(t)
            except ValueError:
                pass
        # self.trapezoids.remove(trapezoid)

    def visualize(self, P=None):
        """
        Visualize the given trapezoidal map with matplotlib
        :return:
        """
        # Draw the trapezoidal map
        for trapezoid in self.trapezoids:
            y_s = []
            # now we need to project a vertical line on the bottom edge
            if trapezoid.left_p == trapezoid.top.p:
                l = trapezoid.bottom
                y = l.slope * trapezoid.left_p.x + l.intercept
                y_s.extend([y, trapezoid.left_p.y])
            elif trapezoid.left_p == trapezoid.bottom.p:
                l = trapezoid.top
                y = l.slope * trapezoid.left_p.x + l.intercept
                y_s.extend([trapezoid.left_p.y, y])
            else:
                l = trapezoid.bottom
                y = l.slope * trapezoid.left_p.x + l.intercept
                y_s.append(y)
                l = trapezoid.top
                y = l.slope * trapezoid.left_p.x + l.intercept
                y_s.append(y)

            if trapezoid.right_p == trapezoid.top.p:
                l = trapezoid.bottom
                y = l.slope * trapezoid.right_p.x + l.intercept
                y_s.extend([trapezoid.right_p.y, y])
            elif trapezoid.right_p == trapezoid.bottom.p:
                l = trapezoid.top
                y = l.slope * trapezoid.right_p.x + l.intercept
                y_s.extend([y, trapezoid.right_p.y])
            else:
                l = trapezoid.top
                y = l.slope * trapezoid.right_p.x + l.intercept
                y_s.append(y)
                l = trapezoid.bottom
                y = l.slope * trapezoid.right_p.x + l.intercept
                y_s.append(y)

            y_s.append(y_s[0])
            x_s = [trapezoid.left_p.x, trapezoid.left_p.x, trapezoid.right_p.x, trapezoid.right_p.x, trapezoid.left_p.x]
            plt.plot(x_s, y_s, 'k')

        # Draw the polygon also if there
        if P:
            x_s = [p.x for p in P.V]
            y_s = [p.y for p in P.V]
            plt.fill(x_s, y_s, 'b')

        # Display
        plt.show()

    def visualize_graph(self):
        assert isinstance(self.G, DAG)
        G = nx.DiGraph()
        for n in self.G.in_order(self.G.root):
            if n.left_child:
                G.add_edge(n, n.left_child)
            if n.right_child:
                G.add_edge(n, n.right_child)
        pos = self.hierarchy_pos(G, root=self.G.root, is_dag=nx.is_directed_acyclic_graph(G))
        nx.draw(G, pos=pos)
        fig = plt.gcf()

        # Create labels
        x_s = [p[0] for p in pos.values()]
        y_s = [p[1] for p in pos.values()]
        af = MatPlotAnnotater(x_s, y_s, pos.keys(), 'motion_notify_event')
        fig.canvas.mpl_connect('motion_notify_event', af)

        # Display and return
        plt.show()
        return G

    def hierarchy_pos(self, G, root, is_dag, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5,
                      pos=None, parent=None):
        """
        If there is a cycle that is reachable from root, then this will see infinite recursion.
        G: the graph
        root: the root node of current branch
        width: horizontal space allocated for this branch - avoids overlap with other branches
        vert_gap: gap between levels of hierarchy
        vert_loc: vertical location of root
        xcenter: horizontal location of root
        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch.
        """
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        neighbors = G.neighbors(root)
        if (not is_dag) and parent is not None:
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / len(neighbors)
            nextx = xcenter - width / 2 - dx / 2
            for neighbor in neighbors:
                nextx += dx
                pos = self.hierarchy_pos(G, neighbor, is_dag=is_dag, width=dx, vert_gap=vert_gap,
                                         vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                         pos=pos, parent=root)
        return pos

    def __repr__(self):
        return '<Trapezoidal map -> Trapezoids: %s>' % (str(self.trapezoids))
