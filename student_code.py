"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import sys
from types import SimpleNamespace

from Agents import Agents
from Pokemon import Pokemon
from api.DiGraph import DiGraph
from api.GraphAlgo import GraphAlgo
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *


# init pygame
def get_graph(graph_json):
    graph = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
    g = DiGraph()
    for node in graph.Nodes:
        x1, y1, _ = node.pos.split(',')
        node.pos = (float(x1), float(y1), 0)
        g.add_node(node.id, node.pos)
    for edge in graph.Edges:
        g.add_edge(edge.src, edge.dest, edge.w)
    return g


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


class Student_code:
    def __init__(self):
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.PORT = 6666
        self.HOST = '127.0.0.1'
        pygame.init()
        self.screen = display.set_mode((self.WIDTH, self.HEIGHT), depth=32, flags=RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.client = Client()
        self.client.start_connection(self.HOST, self.PORT)
        self.pokemons = self.client.get_pokemons()
        print(self.pokemons)
        graph_json = self.client.get_graph()
        self.graph = get_graph(graph_json)
        print(self.graph.Edges)
        self.list_pok = self.get_list_pokemon()
        self.paint_g = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        for node in self.paint_g.Nodes:
            x1, y1, _ = node.pos.split(',')
            node.pos = SimpleNamespace(x=float(x1), y=float(y1))
        self.min_x = min(list(self.paint_g.Nodes), key=lambda n1: n1.pos.x).pos.x
        self.min_y = min(list(self.paint_g.Nodes), key=lambda n1: n1.pos.y).pos.y
        self.max_x = max(list(self.paint_g.Nodes), key=lambda n1: n1.pos.x).pos.x
        self.max_y = max(list(self.paint_g.Nodes), key=lambda n1: n1.pos.y).pos.y
        self.paths = dict()
        self.ag = None
        print("9**: ", self.paint_g.Nodes[9].pos)
        print("8**: ", self.paint_g.Nodes[8].pos)
        print("9: ", self.graph.get_all_v()[9].x, ",", self.graph.get_all_v()[9].y)
        print("8: ", self.graph.get_all_v()[8].x, ",", self.graph.get_all_v()[8].y)
        self.game()

    def game(self):
        pygame.font.init()
        print(self.pokemons)
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        radius = 15

        src = self.edge(self.list_pok[0])[0]
        print("start:", src)
        self.client.add_agent("{\"id\":" + str(src) + "}")
        self.client.add_agent("{\"id\":1}")
        self.client.add_agent("{\"id\":2}")
        self.client.add_agent("{\"id\":3}")
        self.client.start()
        while self.client.is_running() == 'true':
            pokemons = json.loads(self.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            self.list_pok = self.get_list_pokemon()
            for p in pokemons:
                x, y, _ = p.pos.split(',')
                p.pos = SimpleNamespace(x=self.my_scale(float(x), x=True), y=self.my_scale(float(y), y=True))

            agents = json.loads(self.client.get_agents(),
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for a in agents:
                x, y, _ = a.pos.split(',')
                a.pos = SimpleNamespace(x=self.my_scale(
                    float(x), x=True), y=self.my_scale(float(y), y=True))
            self.ag = self.get_list_agents()
            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            self.screen.fill(Color(0, 0, 0))

            # draw nodes
            for n in self.paint_g.Nodes:
                x = self.my_scale(n.pos.x, x=True)
                y = self.my_scale(n.pos.y, y=True)
                # its just to get a nice antialiased circle
                gfxdraw.filled_circle(self.screen, int(x), int(y), radius, Color(64, 80, 174))
                gfxdraw.aacircle(self.screen, int(x), int(y), radius, Color(255, 255, 255))
                # draw the node id
                id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
                rect = id_srf.get_rect(center=(x, y))
                self.screen.blit(id_srf, rect)
            # draw edges
            for e in self.paint_g.Edges:
                # find the edge nodes
                src = next(n for n in self.paint_g.Nodes if n.id == e.src)
                dest = next(n for n in self.paint_g.Nodes if n.id == e.dest)
                # scaled positions
                src_x = self.my_scale(src.pos.x, x=True)
                src_y = self.my_scale(src.pos.y, y=True)
                dest_x = self.my_scale(dest.pos.x, x=True)
                dest_y = self.my_scale(dest.pos.y, y=True)
                # draw the line
                pygame.draw.line(self.screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))
            # draw agents
            for agent in agents:
                pygame.draw.circle(self.screen, Color(122, 61, 23),
                                   (int(agent.pos.x), int(agent.pos.y)), 10)
            # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
            for p in pokemons:
                pygame.draw.circle(self.screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

            # update screen changes
            display.update()

            self.clock.tick(60)
            self.algo()
            self.client.move()

    def algo(self):
        print("path1:", self.ag[0].path)
        p = []
        for agent in self.ag.keys():
            m = sys.maxsize
            i = None
            p = []
            if not self.ag[agent].path:
                for pok in self.list_pok:
                    edge = self.edge(pok)
                    src = edge[0]
                    dest = edge[1]
                    graphAlgo = GraphAlgo(self.graph)
                    ans = graphAlgo.TSP([self.ag[agent].src, src, dest])
                    dist = ans[1] + self.graph.Edges[src][dest]
                    path = ans[0]
                    path.append(dest)
                    if dist < m:
                        m = dist
                        i = pok
                        p = path
                if i != -1 and p != []:
                    self.ag[agent].path = p
                    self.ag[agent].pok = i
        for i in self.ag.keys():
            if self.ag[i].path:
                if self.ag[i].path.__len__ == 2:
                    x = self.ag[i].path[0]
                    y = self.ag[i].path[1]
                    t = self.ag[i].pok.type
                    if x < y and t < 0:
                        self.ag[i].path.insert(2, x)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(i) + ', "next_node_id":' + str(self.ag[i].path[0]) + '}')
                self.ag[i].src = self.ag[i].path[0]
                if len(self.ag[i].path) > 1:
                    self.ag[i].dest = self.ag[i].path[1]
                    self.ag[i].path.remove(self.ag[i].path[0])
                else:
                    self.ag[i].dest = -1
                    self.ag[i].path.remove(self.ag[i].path[0])

        for i in self.ag.keys():
            self.paths[i] = self.ag[i].path

        ttl = self.client.time_to_end()
        print(ttl, self.client.get_info())

    def get_list_pokemon(self):
        pok = []
        pokemons = json.loads(self.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        for p in pokemons:
            x1, y1, _ = p.pos.split(',')
            pos1 = (x1, y1)
            t = Pokemon(p.type, p.value, pos1, self.graph)
            pok.append(t)
        return pok

    def get_list_agents(self):
        ag = dict()
        agents = json.loads(self.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for a in agents:
            x, y, _ = a.pos.split(',')
            pos = (x, y)
            temp = Agents(a.id, a.value, a.src, a.dest, a.speed, pos, self.graph)
            if self.paths != {}:
                print(a.id)
                temp.path = self.paths[a.id]
            ag[a.id] = temp
            a.pos = SimpleNamespace(x=self.my_scale(float(x), x=True), y=self.my_scale(float(y), y=True))
        return ag

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def shortest_dist(self, agent_id, node_id: int) -> float:
        if self.ag[agent_id].dest == -1:
            graphAlgo = GraphAlgo(self.graph)
            dist = graphAlgo.shortest_path(self.ag[agent_id].src, node_id)
            return dist
        else:
            ans = (sys.maxsize, -1)
            return ans

    def edge(self, pok: Pokemon):
        for s in self.graph.Edges.keys():
            for dest in self.graph.Edges[s].keys():
                node_src = self.graph.get_all_v()[s]
                node_dest = self.graph.get_all_v()[dest]
                pos_src = (node_src.x, node_src.y)
                pos_dest = (node_dest.x, node_dest.y)
                if line(pos_src, pos_dest, pok):
                    if (pok.type < 0 and s > dest) or (pok.type > 0 and s < dest):
                        ans = (s, dest)
                        return ans


def line(pos1: tuple, pos2: tuple, pok: Pokemon):
    pos3 = (pok.x, pok.y)
    m = (pos1[1] - pos2[1]) / (pos1[0] - pos2[0])
    n = pos1[1] - m * pos1[0]
    ans = m * pos3[0] + n
    if 0.000001 > pos3[1] - ans > -0.000001:
        return True
    # pos3 = (pok.x, pok.y)
    # d1_3 = distance(pos1, pos3)
    # d2_3 = distance(pos2, pos3)
    # d1_2 = distance(pos1, pos2)
    # ans1 = d1_3 + d2_3
    # ans2 = d1_2
    # if 0.0001 > ans1 - ans2 > -0.0001:
    #     return True


def distance(pos1: tuple, pos2: tuple):
    xx = math_pow((pos1[0] - pos2[0]), 2)
    yy = math_pow((pos1[1] - pos2[1]), 2)
    xy = xx + yy
    ans = math.sqrt(xy)
    return ans


def math_pow(a, b):
    i = 0
    ans = 0
    while i < b:
        ans *= a
    return ans


if __name__ == '__main__':
    Student_code()
"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

#
# def the_closet(agents:list,pokemon:Pokemon):
#     for i in range(agents):

# game over:
