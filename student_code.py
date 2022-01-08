"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import sys
import time
from asyncio import wait
from types import SimpleNamespace

from Agents import Agents
from Pokemon import Pokemon
from api.DiGraph import DiGraph
from api.GraphAlgo import GraphAlgo
from Rect_text import Rect_text
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *


class Student_code:
    def __init__(self):
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.PORT = 6666
        self.HOST = '127.0.0.1'
        pygame.init()
        self.screen = display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.client = Client()
        self.client.start_connection(self.HOST, self.PORT)
        self.pokemons = self.client.get_pokemons()
        print(self.pokemons)
        graph_json = self.client.get_graph()
        self.graph = get_graph(graph_json)
        self.pok = []
        self.list_pok = None
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
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        self.game()

    def check_click(self, stop_button):
        mouse_pos = pygame.mouse.get_pos()
        if stop_button.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.client.stop()
                pygame.quit()
                exit(0)

    def game(self):
        pygame.font.init()
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        FONT2 = pygame.font.SysFont('comicsansms', 25, bold=True)
        radius = 15
        for pok in self.list_pok:
            src = self.edge(pok)[0]
            self.client.add_agent("{\"id\":" + str(src) + "}")
        self.client.start()

        while self.client.is_running() == 'true':
            if int(self.client.time_to_end()) < 100:
                self.client.stop()
                pygame.quit()
                exit(0)

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
                    self.client.stop_connection()
                    pygame.quit()
                    exit(0)

            self.screen.fill(0)

            background = pygame.image.load('imags/background.jpg')
            change_scale = pygame.transform.scale(background, (1080, 720))
            background_rect = background.get_rect(topleft=(0, 0))
            self.screen.blit(change_scale, background_rect)

            stop_button = Rect_text('stop', 75, 35, (25, 25), self.screen, FONT, (255, 255, 255), (255, 0, 0))
            r = pygame.Rect((25, 25), (85, 45))
            pygame.draw.rect(self.screen, (157, 157, 157), r)
            pygame.draw.rect(self.screen, stop_button.top_color, stop_button.top_rect)
            self.screen.blit(stop_button.text_surf, stop_button.text_rect)

            grade = 'grade=' + str(self.get_grade())
            g_srf = FONT2.render(grade, True, Color(255, 255, 255))
            rect_srf = g_srf.get_rect(center=(920, 630))
            self.screen.blit(g_srf, rect_srf)

            ttl = 'ttl=' + str(self.client.time_to_end())
            ttl_srf = FONT2.render(ttl, True, Color(255, 255, 255))
            rect2_srf = ttl_srf.get_rect(center=(920, 675))
            self.screen.blit(ttl_srf, rect2_srf)

            level = 'level=' + str(self.get_level())
            level_srf = FONT2.render(level, True, Color(255, 255, 255))
            rect4_srf = level_srf.get_rect(center=(990, 50))
            self.screen.blit(level_srf, rect4_srf)
            self.check_click(stop_button)

            for n in self.paint_g.Nodes:
                x = self.my_scale(n.pos.x, x=True)
                y = self.my_scale(n.pos.y, y=True)
                gfxdraw.filled_circle(self.screen, int(x), int(y), radius, Color(64, 80, 174))
                gfxdraw.aacircle(self.screen, int(x), int(y), radius, Color(255, 255, 255))
                id_srf = FONT.render(str(n.id), True, Color(0, 0, 0))
                rect3_srf = id_srf.get_rect(center=(x, y))
                self.screen.blit(id_srf, rect3_srf)

            for e in self.paint_g.Edges:
                src = next(n for n in self.paint_g.Nodes if n.id == e.src)
                dest = next(n for n in self.paint_g.Nodes if n.id == e.dest)
                src_x = self.my_scale(src.pos.x, x=True)
                src_y = self.my_scale(src.pos.y, y=True)
                dest_x = self.my_scale(dest.pos.x, x=True)
                dest_y = self.my_scale(dest.pos.y, y=True)
                pygame.draw.line(self.screen, Color(255, 255, 255), (src_x, src_y), (dest_x, dest_y))

            for agent in agents:
                a = pygame.image.load('imags/player.png')
                a_scale = pygame.transform.scale(a, (30, 30))
                a_rect = a.get_rect(topleft=(int(agent.pos.x), int(agent.pos.y)))
                self.screen.blit(a_scale, a_rect)

            FONT3 = pygame.font.SysFont('Arial', 15, bold=True)
            for p in pokemons:
                if p.type > 0:
                    pika = pygame.image.load('imags/pikachu 2.png')
                else:
                    pika = pygame.image.load('imags/pikachu.png')
                pika_scale = pygame.transform.scale(pika, (30, 30))
                pika_rect = pika.get_rect(topleft=(int(p.pos.x), int(p.pos.y)))
                self.screen.blit(pika_scale, pika_rect)
                value_srf = FONT3.render(str(p.value), True, Color(255, 255, 255))
                rect3 = value_srf.get_rect(center=(int(p.pos.x), int(p.pos.y)))
                self.screen.blit(value_srf, rect3)

            display.update()

            self.clock.tick(10)
            self.algo()
            self.client.move()

    def algo(self):
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
            # print("path1:", self.ag[0].path)
            if self.ag[i].path:
                # print("path2:", self.ag[0].path)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(i) + ', "next_node_id":' + str(self.ag[i].path[0]) + '}')
                self.ag[i].src = self.ag[i].path[0]
                if len(self.ag[i].path) > 1:
                    self.ag[i].dest = self.ag[i].path[1]
                    self.ag[i].path.remove(self.ag[i].path[0])
                elif len(self.ag[i].path) == 1:
                    self.ag[i].dest = -1
                    self.ag[i].path.remove(self.ag[i].path[0])
                    temp = inside(self.ag[i].pok, self.list_pok)
                    if temp != -1:
                        self.pok.insert(temp, True)
                # print("pok:", self.ag[i].pok)

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
            if self.ag != None:
                temp.pok = self.ag[a.id].pok
            if self.paths != {}:
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

    def get_grade(self):
        info_json = self.client.get_info()
        info = json.loads(info_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        return info.GameServer.grade

    def get_level(self):
        info_json = self.client.get_info()
        info = json.loads(info_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        return info.GameServer.game_level


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


def math_pow(a, b):
    i = 0
    ans = 0
    while i < b:
        ans *= a
    return ans


def eq(p1: Pokemon, p2: Pokemon):
    if p1.x == p2.x and p1.y == p2.y and p1.type == p2.type and p1.value == p2.value and p1.catch == p2.catch:
        return True
    return False


def inside(p: Pokemon, l_p: list):
    for i in range(len(l_p)):
        if eq(p, l_p[i]):
            return i
    return -1


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def line(pos1: tuple, pos2: tuple, pok: Pokemon):
    pos3 = (pok.x, pok.y)
    m = (pos1[1] - pos2[1]) / (pos1[0] - pos2[0])
    n = pos1[1] - m * pos1[0]
    ans = m * pos3[0] + n
    if 0.000001 > pos3[1] - ans > -0.000001:
        return True


def distance(pos1: tuple, pos2: tuple):
    xx = math_pow((pos1[0] - pos2[0]), 2)
    yy = math_pow((pos1[1] - pos2[1]), 2)
    xy = xx + yy
    ans = math.sqrt(xy)
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
