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
        self.x = float(pos[0])
        self.y = float(pos[1])
        self.graph = graph
        self.catch = False
        self.belong=False

    def distance(self, i: int):
        x1 = self.graph.get_all_v()[i].x
        y1 = self.graph.get_all_v()[i].y
        xx = math.pow((x1 - self.x), 2)
        yy = math.pow((y1 - self.y), 2)
        xy = xx + yy
        ans = math.sqrt(xy)
        return ans

    def closet_node(self, k):
        m = sys.maxsize
        j = -1
        for i in self.graph.Nodes.keys():
            if i == k:
                continue
            d = self.distance(i)
            if d < m:
                m = d
                j = i
        return j

    def edge(self):
        src = self.closet_node(-1)
        dest = self.closet_node(src)
        ans = (src, dest)
        return ans

    def __str__(self):
        return "type: " + str(self.type) + " value: " + str(self.value) + " pos:( " + str(self.x) + "," + \
               str(self.y) + ")" + " catch: " + str(self.catch)

    def __repr__(self):
        return "type: " + str(self.type) + " value: " + str(self.value) + " pos:( " + str(self.x) + "," + \
               str(self.y) + ")" + " catch: " + str(self.catch)
