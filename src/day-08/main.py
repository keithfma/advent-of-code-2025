from scipy.spatial import KDTree
from networkx import Graph, connected_components
import numpy as np
from operator import attrgetter
from dataclasses import dataclass, replace


EXAMPLE = 'example.txt'
REAL = 'input.txt'

type Point = tuple[int, int, int]


def parse(path: str) -> list[Point]:
    with open(path, 'r') as f:
        return [
            tuple(int(x) for x in line.strip().split(','))
            for line in f.readlines()
        ]


@dataclass
class NbrInfo:
    # index of the node itself
    self_idx: int  
    # index of the nth nearest neighbor
    nbr_idx: int
    # how far from the node to its nth nearest neighbor
    distance: float 
    # which nearest neighbor is it?
    nth_nearest: int


def connect_n(p: list[Point], n: int) -> int:
    """Connect the N closest pairs of points, and return the product of the size of the 3 largest circiuts that result"""
    # use index to refer to each node
    nodes = np.arange(len(p))

    # initialize the list of nearest neighbors 
    nbrs: list[NbrInfo] = []
    t = KDTree(p)
    # note: k=[2] selects the *2nd* nearest neighbor, since 1st nearest is self 
    distances, nbr_indexes = (arr.squeeze() for arr in t.query(t.data, k=[2]))
    for self_idx, (distance, nbr_idx) in enumerate(zip(distances, nbr_indexes)):
        nbrs.append(NbrInfo(self_idx, int(nbr_idx), float(distance), 2))

    # build graph one edge at a time, finding the next-nearest-neighbor each time we consume an edge
    g = Graph()
    while g.number_of_edges() != n:
        shortest = min(nbrs, key=attrgetter('distance'))
        # add the edge
        g.add_edge(shortest.self_idx, shortest.nbr_idx)
        # find the next nearest neighbor for that node
        next_dist, next_idx = (arr.squeeze() for arr in t.query(t.data[shortest.self_idx, :], k=[shortest.nth_nearest + 1]))
        nbrs[shortest.self_idx] = replace(shortest, nbr_idx=int(next_idx), distance=float(next_dist), nth_nearest=shortest.nth_nearest + 1)

    # compute product of the size of the 3 largest connected components
    total = 1
    for circuit in sorted(connected_components(g), key=len, reverse=True)[:3]:
        total *= len(circuit)
        
    return total


if __name__ == '__main__':

    print('Example')
    points = parse(EXAMPLE)
    print(f'Part 1: {connect_n(points, n=10)}')

    print('Real')
    points = parse(REAL)
    print(f'Part 1: {connect_n(points, n=1000)}')