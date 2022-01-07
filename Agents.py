import sys

from api.DiGraph import DiGraph
from api.GraphAlgo import GraphAlgo


class Agents:
    def __init__(self, i: int, value: float, src: int, dest: int, speed: float, pos: tuple, graph: DiGraph):
        self.id = i
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.x = pos[0]
        self.y = pos[1]
        self.graph = graph
        self.moving = False
        self.path = []
        self.pok = None

    def shortest_dist(self, i: int) -> float:
        if self.dest != -1:
            graphAlgo = GraphAlgo(self.graph)
            dist = graphAlgo.shortest_path(self.src, i)[0]
            return dist
        else:
            return sys.maxsize
