import json
import sys

from typing import List
import matplotlib.pyplot as plt
from api.DiGraph import DiGraph
from api.GraphAlgoInterface import GraphAlgoInterface
from api.GraphInterface import GraphInterface
from api.Node import Node
from api.SaveJson import SaveJson


def min_val(nodes: dict()) -> int:  # return the node with minimum weigh that still "white"
    # -help function to the algo "shortest path"
    m = sys.maxsize
    temp = -1
    for i in nodes.keys():
        if nodes[i].info == "white":
            if nodes[i].weigh < m:
                m = nodes[i].weigh
                temp = nodes[i].id

    if temp == -1:
        for i in nodes.keys():
            if nodes[i].info == "white":
                temp = nodes[i].id
                break

    return temp


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = None):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:  # load the graph from json
        g = DiGraph()
        with open(file_name, "r") as fp:
            di = json.load(fp)
            for k in di["Nodes"]:
                i = int(k["id"])
                if k.__len__() > 1:
                    if type(k["pos"]) == list:
                        pos = k["pos"]
                        t = (pos[0], pos[1], pos[2])
                    else:
                        pos = (k["pos"]).split(',')
                        t = (pos[0], pos[1], pos[2])
                    g.add_node(i, t)
                else:
                    g.add_node(i)
            for k in di["Edges"]:
                src = k["src"]
                dest = k["dest"]
                w = k["w"]
                g.add_edge(src, dest, w)
        self.__init__(g)
        if self.get_graph() == g:
            return True
        return False

    def save_to_json(self, file_name: str) -> bool:  # save the graph in json format,
        # use class "SaveJson" that return a graph  that have the same format like A0,...,A5,T0
        s_j = SaveJson(self.graph)
        with open(file_name, "w") as f:
            json.dump(s_j, indent=4, fp=f, default=lambda m: m.__dict__)
        g_temp = GraphAlgo()
        if g_temp.load_from_json(file_name):
            return True
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        # use function "path" that return the shortest dist and the path
        nodes = self.path(id1, 1)
        if id1 == id2:
            ans = (0, [])
        elif nodes[id2].weigh == sys.maxsize:
            ans = (float('inf'), [])
        else:
            w = nodes[id2].weigh
            p = []
            p.insert(0, id2)
            j = nodes[id2].tag
            while j != id1:
                p.insert(0, j)
                j = nodes[j].tag
            p.insert(0, id1)
            ans = (w, p)

        return ans

    def path(self, id1: int, key: int):  # help function to the shortest path,tsp and center
        nodes = dict()
        for i in self.graph.Nodes.keys():
            n = Node(i, self.graph.Nodes[i])
            if i in self.graph.Edges[id1]:
                n.weigh = self.graph.Edges[id1][i]
            else:
                n.weigh = sys.maxsize
            n.tag = -1
            n.info = "white"
            nodes[i] = n
        nodes[id1].weigh = 0
        nodes[id1].tag = 0
        i = id1
        t = 0
        size = self.get_graph().v_size()
        while t < size:
            if nodes[i].info != "white":
                t += 1
                continue
            nodes[i].info = "black"
            for j in self.graph.Edges[i].keys():
                temp_j = nodes[j].weigh
                temp_i = nodes[i].weigh
                if temp_i != sys.maxsize:
                    w = self.graph.Edges[i][j]
                    m = min(temp_j, temp_i + w)
                    nodes[j].weigh = m
                if temp_j != nodes[j].weigh or i == id1:
                    nodes[j].tag = i
            i = min_val(nodes)
            t += 1
        if key == 1:
            return nodes
        m = -sys.maxsize
        for i in nodes:
            if nodes[i].weigh > m:
                m = nodes[i].weigh
        return m

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        # return the shortest path that visit all the node in the list
        if node_lst.__len__() == 0:
            ans = ([], float('inf'))
            return ans
        if node_lst.__len__() == 1:
            return node_lst, 0
        count = 0
        n1 = node_lst[0]
        ans = []
        while node_lst.__len__() != 0:
            k = -1
            m = sys.maxsize
            for n2 in node_lst:
                if n1 == n2:
                    continue
                l_temp = self.help_tsp(n1, n2)
                if l_temp is None:
                    ans = ([], float('inf'))
                    return ans
                temp = l_temp[0]
                del l_temp[0]
                if temp < m:
                    m = temp
                    k = n2
            if node_lst.__len__() == 1:
                ans.append(n1)
                node_lst.remove(n1)
                break
            if m == sys.maxsize and node_lst.__len__() != 1:
                ans = ([], float('inf'))
                return ans
            t = self.shortest_path(n1, k)
            l_temp = t[1]
            count += t[0]
            for i in l_temp:
                if i == k:
                    continue
                ans.append(i)
            node_lst.remove(n1)
            n1 = k
        li = [ans, count]
        return li

    def help_tsp(self, id1, id2):  # help function to the tsp
        my_list = self.shortest_path(id1, id2)
        if my_list == (float('inf'), []):
            return None
        w = my_list[0]
        li = my_list[1]
        li.insert(0, w)
        return li

    def is_connected(self) -> bool:  # check if the graph is connected-help function to center
        v = dict()
        for i in self.graph.Nodes.keys():
            v[i] = False
        if self.graph.v_size() == 0:
            return True
        q = []
        for k in self.graph.Nodes.keys():
            q.append(k)
            break
        while q.__len__() != 0:
            temp = q[0]
            del q[0]
            for i in self.graph.Edges[temp]:
                if v[i]:
                    continue
                q.append(i)
                v[i] = True
        for i in v.keys():
            if not v[i]:
                return False
            v[i] = False
        di = self.revers()
        for k in self.graph.Nodes.keys():
            q.append(k)
            break
        while q.__len__() != 0:
            temp = q[0]
            del q[0]
            for i in di[temp]:
                if v[i]:
                    continue
                q.append(i)
                v[i] = True
        for i in v.keys():
            if not v[i]:
                return False
        return True

    def revers(self) -> dict(dict()):  # transposes the graph
        ans = dict(dict())
        for i in self.graph.Edges:
            ans[i] = {}
        for i in self.graph.Edges:
            for j in self.graph.Edges[i]:
                w = self.graph.Edges[i][j]
                ans[j][i] = w
        return ans

    def centerPoint(self) -> (int, float):  # find the node that have the shortest distance to it's farthest node.
        if not self.is_connected():
            return
        m = sys.maxsize
        k = -1
        for i in self.graph.Nodes.keys():
            temp = self.path(i, 0)
            if temp < m:
                m = temp
                k = i
        ans = (k, m)
        return ans

    def plot_graph(self) -> None:  # show the graph
        for v in self.graph.Nodes.keys():
            t = self.graph.Nodes[v]
            x = float(t[0])
            y = float(t[1])
            plt.plot(x, y, markersize=4, marker="o", color="red")
            plt.text(x, y, str(v), color="green", fontsize=12)
            for w in self.graph.Edges[v].keys():
                t1 = self.graph.Nodes[w]
                x_ = float(t1[0])
                y_ = float(t1[1])
                plt.annotate("", xy=(x, y), xytext=(x_, y_), arrowprops=dict(arrowstyle="<-"))

        plt.show()
