from unittest import TestCase


from api.DiGraph import DiGraph
from api.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
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
    g_algo = GraphAlgo(g)
    g1 = DiGraph()
    for n in range(5):
        g1.add_node(n)
    g1.add_edge(0, 1, 1)
    g1.add_edge(0, 4, 5)
    g1.add_edge(1, 0, 1.1)
    g1.add_edge(1, 2, 1.3)
    g1.add_edge(1, 3, 1.9)
    g1.add_edge(2, 3, 1.1)
    g1.add_edge(3, 4, 2.1)
    g1.add_edge(4, 2, .5)
    g1_algo = GraphAlgo(g1)

    def test_get_graph(self):
        self.assertEqual(self.g_algo.get_graph(), self.g)

    def test_load_from_json(self):
        g1_algo = GraphAlgo(self.g)
        self.assertEqual(g1_algo.load_from_json("A0.json"), True)

    def test_save_to_json(self):
        self.assertEqual(self.g_algo.save_to_json("test.json"), True)

    def test_shortest_path(self):
        self.assertEqual(self.g_algo.shortest_path(0, 3), (3.4, [0, 1, 2, 3]))

    def test_tsp(self):
        self.assertEqual(self.g1_algo.TSP([1, 2, 4]), [[1, 2, 3, 4], 4.5])

    def test_is_connected(self):
        self.assertEqual(False, self.g1_algo.is_connected())
        g1_algo = GraphAlgo(self.g)
        g1_algo.load_from_json("A0.json")
        self.assertEqual(True, g1_algo.is_connected())

    def test_center_point(self):
        g1 = GraphAlgo()
        g1.load_from_json("A0.json")
        self.assertEqual(g1.centerPoint(), (7, 6.806805834715163))
        g1.load_from_json("A1.json")
        self.assertEqual(g1.centerPoint(), (8, 9.925289024973141))
        g1.load_from_json("A2.json")
        self.assertEqual(g1.centerPoint(), (0, 7.819910602212574))
        g1.load_from_json("A3.json")
        self.assertEqual(g1.centerPoint(), (2, 8.182236568942237))
        g1.load_from_json("A4.json")
        self.assertEqual(g1.centerPoint(), (6, 8.071366078651435))
        g1.load_from_json("A5.json")
        self.assertEqual(g1.centerPoint(), (40, 9.291743173960954))

    def test_plot_graph(self):
        self.g_algo.plot_graph()
