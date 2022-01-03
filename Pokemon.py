import json
from types import SimpleNamespace

import client


class Pokemon:
    def __init__(self, t: int, value: float, pos: tuple):
        self.type = t
        self.value = value
        self.x = pos[0]
        self.y = pos[1]
