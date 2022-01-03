import json
import math
import sys
from types import SimpleNamespace
from api.DiGraph import DiGraph
from api.GraphAlgo import GraphAlgo

import client


class Pokemon:
    def __init__(self, t: int, value: float, pos: tuple, graph: DiGraph):
        self.type = t
        self.value = value
        self.x = pos[0]
        self.y = pos[1]
        self.graph = graph

    def distance(self, i: int):
        x1 = self.graph.get_all_v()[i].x
        y1 = self.graph.get_all_v()[i].y
        xx = math.pow(x1 - self.x, 2)
        yy = math.pow(y1 - self.y, 2)
        xy = xx + yy
        ans = math.sqrt(xy)
        return ans

    def closet_node(self):
        m = sys.maxsize
        j = -1
        for i in self.graph.Nodes.keys():
            d = self.distance(i)
            if d < m:
                m = d
                j = i
        return j
