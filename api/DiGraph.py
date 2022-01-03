from api.GraphInterface import GraphInterface
from api.Node import Node
import random


class DiGraph(GraphInterface):
    def __init__(self):
        self.Edges = dict(dict())
        self.Nodes = dict()
        self.v_s = 0
        self.e_s = 0
        self.mc = 0

    def v_size(self) -> int:  # return how much node in the graph
        return self.v_s

    def e_size(self) -> int:  # return how much edge int the graph
        return self.e_s

    def get_all_v(self) -> dict:  # return a dict with all the node
        my_dict = dict()
        for i in self.Nodes.keys():
            temp1 = self.all_out_edges_of_node(i).__len__()
            temp2 = self.all_in_edges_of_node(i).__len__()
            n = Node(i, self.Nodes[i])
            n.edges_out = temp1
            n.edges_in = temp2
            my_dict[i] = n
        return my_dict

    def all_in_edges_of_node(self, id1: int) -> dict:  # return a dict with all the edge that enter to the node
        ans = dict()
        if (id1 not in self.Edges):
            return ans
        for i in self.Edges.keys():
            if id1 in self.Edges[i]:
                ans[i] = self.Edges[i][id1]
        return ans

    def all_out_edges_of_node(self, id1: int) -> dict:  # return a dict with all the edge that go out of the node
        ans = dict()
        if id1 not in self.Nodes:
            return ans
        for i in self.Edges[id1]:
            ans[i] = self.Edges[id1][i]
        return ans

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:  # insert edge to the graph
        if (id1 not in self.Nodes or id2 not in
                self.Nodes or weight < 0 or id2 in self.Edges[id1]):
            return
        self.Edges[id1][id2] = weight
        self.e_s += 1
        self.mc += 1

        if id2 in self.Edges[id1]:
            return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:  # insert node to the graph
        if node_id in self.Nodes:
            return
        if pos == None:
            x, y, z = random.uniform(0, 100), random.uniform(0, 100), 0
            self.Nodes[node_id] = (x, y, z, "None")
        else:
            self.Nodes[node_id] = pos
        self.Edges[node_id] = {}
        self.mc += 1
        self.v_s += 1
        if node_id in self.Nodes:
            return True
        else:
            return False

    def remove_node(self, node_id: int) -> bool:  # delete node from the graph
        if node_id not in self.Nodes:
            return False
        del self.Edges[node_id]
        del self.Nodes[node_id]
        for i in self.Edges.keys():
            if node_id in self.Edges[i].keys():
                del self.Edges[i][node_id]
                self.e_s -= 1
        self.v_s -= 1
        self.mc += 1
        if node_id not in self.Nodes:
            return True
        else:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:  # delete edge from the graph
        if (node_id1 not in self.Nodes or node_id2 not in
                self.Nodes or node_id2 not in self.Edges[node_id1]):
            return
        del self.Edges[node_id1][node_id2]
        self.e_s -= 1
        self.mc += 1
        if node_id2 not in self.Edges[node_id1]:
            return True
        else:
            return False

    def __str__(self):  # to print the graph
        s = "Graph: |V|=" + str(self.v_s) + " , |E|=" + str(self.e_s)
        return s
