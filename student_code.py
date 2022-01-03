"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace

from Agents import Agents
from Pokemon import Pokemon
from api.DiGraph import DiGraph
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
        g.add_node(node.id)
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
        pokemons_obj = json.loads(self.pokemons, object_hook=lambda d: SimpleNamespace(**d))
        print(self.pokemons)
        graph_json = self.client.get_graph()
        self.graph = get_graph(graph_json)
        self.list_pok = self.get_list_pokemon()
        self.paint_g = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        for node in self.paint_g.Nodes:
            x1, y1, _ = node.pos.split(',')
            node.pos = SimpleNamespace(x=float(x1), y=float(y1))
        self.min_x = min(list(self.paint_g.Nodes), key=lambda n1: n1.pos.x).pos.x
        self.min_y = min(list(self.paint_g.Nodes), key=lambda n1: n1.pos.y).pos.y
        self.max_x = max(list(self.paint_g.Nodes), key=lambda n1: n1.pos.x).pos.x
        self.max_y = max(list(self.paint_g.Nodes), key=lambda n1: n1.pos.y).pos.y
        self.game()

    def game(self):
        pygame.font.init()
        print(self.pokemons)
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        radius = 15

        self.client.add_agent("{\"id\":0}")
        # client.add_agent("{\"id\":1}")
        # client.add_agent("{\"id\":2}")
        # client.add_agent("{\"id\":3}")
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
            ag = self.get_list_agents()
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
                print("Pokemon: ", p)
                pygame.draw.circle(self.screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

            # update screen changes
            display.update()

            # refresh rate
            self.clock.tick(60)

            # choose next edge

            self.algo(agents)

            self.client.move()

    def algo(self, agents):
        for agent in agents:
            if agent.dest == -1:
                next_node = (agent.src - 1) % len(self.paint_g.Nodes)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
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
        ag = []
        agents = json.loads(self.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for a in agents:
            x, y, _ = a.pos.split(',')
            pos = (x, y)
            temp = Agents(a.id, a.value, a.src, a.dest, a.speed, pos, self.graph)
            ag.append(temp)
            a.pos = SimpleNamespace(x=self.my_scale(float(x), x=True), y=self.my_scale(float(y), y=True))
        return ag

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)


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
