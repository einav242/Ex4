from api.DiGraph import DiGraph


class SaveJson:
    def __init__(self, g: DiGraph):  # turn the graph to be like A0,...,A5,T0
        self.Edges = [{}]
        self.Nodes = [{}]
        k = 0
        if g is not None:
            for i in g.Edges.keys():
                for j in g.Edges[i]:
                    if k != 0:
                        self.Edges.insert(k, {})
                    self.Edges[k]["src"] = i
                    self.Edges[k]["w"] = g.Edges[i][j]
                    self.Edges[k]["dest"] = j
                    k += 1
            j = 0
            for i in g.Nodes.keys():
                if j != 0:
                    self.Nodes.insert(j, {})
                t = g.Nodes[i]
                if t.__len__ == 3:
                    self.Nodes[j]["pos"] = g.Nodes[i]
                self.Nodes[j]["id"] = i
                j += 1
