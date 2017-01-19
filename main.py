from Polygon import Polygon, Point
from RandomizedIncrementalConstruction import RandomizedIncrementalConstruction
import time
import gc
from LineSweep import LineSweep


def load_input(file_name):
    """
    Loads input, parses input and returns graph data structure
    :param file_name:
    :return:
    """
    with open(file_name, 'r') as file:
        n = int(file.readline())
        V = []

        # Create a polygon
        for i in range(n):
            line = file.readline()
            line = [int(l) for l in line.split()]
            # We add 1 to every value such that we can always make a bounding
            # box around the coordinates s.t. the bounding box does not intersect
            # with for example a point (0, 0)
            V.append(Point(line[0] + 1, line[1] + 1))
        P = Polygon(V)

        return P


if __name__ == '__main__':
    # make polygon based on input
    P = load_input('Data/test_4.txt')

    # Initialize algorithm (also computes the map already)
    times = []
    for i in range(0, 1):
        start = time.time()
        # print('---------------- TEST %d ----------------' % i)
        R = RandomizedIncrementalConstruction(P)
        end = time.time()
        print((end-start)*1000)
        times.append((end-start)*1000)

        # Garbage collection
        if i != 0:
            R = None
            gc.collect()

    # Visualize the map
    T = R.getTrapezoidalMap()
    T.visualize(P)
    # T.visualize_graph()
