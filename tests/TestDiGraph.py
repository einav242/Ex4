from unittest import TestCase

from api.DiGraph import DiGraph


class TestDiGraph(TestCase):
    g = DiGraph()
    for n in range(4):
        g.add_node(n)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 0, 1.1)
    g.add_edge(1, 2, 1.3)
    g.add_edge(2, 3, 1.1)
    g.add_edge(1, 3, 1.9)
    g.remove_edge(1, 3)
    g.add_edge(1, 3, 10)
    g1 = DiGraph()
    for n in range(4):
        g1.add_node(n)
    g1.add_edge(0, 1, 1)
    g1.add_edge(1, 0, 1.1)
    g1.add_edge(1, 2, 1.3)
    g1.add_edge(2, 3, 1.1)
    g1.add_edge(1, 3, 1.9)
    g1.remove_edge(1, 3)
    g1.add_edge(1, 3, 10)

    def test_v_size(self):
        self.assertEqual(self.g.v_size(), 4)

    def test_e_size(self):
        self.assertEqual(self.g.e_size(), 5)

    def test_all_in_edges_of_node(self):
        self.assertEqual(self.g.all_in_edges_of_node(1), {0: 1})

    def test_all_out_edges_of_node(self):
        self.assertEqual(self.g.all_out_edges_of_node(1), {0: 1.1, 2: 1.3, 3: 10})

    def test_get_mc(self):
        self.assertEqual(self.g.get_mc(), 11)

    def test_add_edge(self):
        self.g1.add_edge(0, 2, 6)
        self.assertEqual(self.g1.Edges[0][2], 6)

    def test_add_node(self):
        self.g1.add_node(8, (2, 3))
        self.assertEqual(True, 8 in self.g1.Nodes)
        self.assertEqual(self.g1.Nodes[8], (2, 3))

    def test_remove_node(self):
        self.g1.remove_node(0)
        self.assertEqual(False, 0 in self.g1.Nodes)
        self.assertEqual(True, 0 not in self.g1.Edges[1])

    def test_remove_edge(self):
        self.g1.remove_edge(2, 3)
        self.assertEqual(True, 3 not in self.g1.Edges[2])
