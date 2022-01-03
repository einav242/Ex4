import json
from types import SimpleNamespace

import client


class Pokemon:
    def __init__(self, t: int = None, value: float = None, pos: tuple = None):
        if t is None and value is None:
            self.type = 0
            self.value = -1
            self.x = None
            self.y = None

        else:
            self.type = t
            self.value = value
            if pos is not None:
                self.x = pos[0]
                self.y = pos[1]
            else:
                self.x = None
                self.y = None




