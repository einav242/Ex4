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
        self.belong = False

    def __str__(self):
        return "type: " + str(self.type) + " value: " + str(self.value) + " pos:( " + str(self.x) + "," + \
               str(self.y) + ")" + " catch: " + str(self.catch)

    def __repr__(self):
        return "type: " + str(self.type) + " value: " + str(self.value) + " pos:( " + str(self.x) + "," + \
               str(self.y) + ")" + " catch: " + str(self.catch)
