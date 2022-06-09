import random

from GLOBALS import *


class PosNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = f'{x}_{y}'
        self.neighbours = []


class TargetNode:
    def __init__(self, i, decay_rate=3, min_life=10, max_life=30, lifespan=100, pos=None, req=100):
        self.num = i
        self.name = f'target_{i}'
        self.decay_rate = decay_rate
        self.min_life = min_life
        self.max_life = max_life
        self.lifespan = lifespan
        self.pos = pos
        self.req = req
        self.up_values = []
        self.init()

    def init(self):
        rand_start = random.randint(0, self.lifespan)
        rand_lifelong = random.randint(self.min_life, self.max_life + 1)
        for i in range(self.lifespan):
            up_value = 0.0
            if rand_start <= i <= rand_start + rand_lifelong:
                if rand_start <= i <= rand_start + self.decay_rate:
                    up_value = (i - rand_start) / self.decay_rate

                elif rand_start + rand_lifelong - self.decay_rate <= i <= rand_start + rand_lifelong:
                    up_value = (rand_start + rand_lifelong - i) / self.decay_rate
                else:
                    up_value = 1.0
            self.up_values.append(up_value)


class AgentNode:
    def __init__(self, i, sr=10, pos=None, cred=50):
        self.num = i
        self.name = f'agent_{i}'
        self.sr = sr
        self.start_pos = pos
        self.pos = pos
        self.cred = cred


def main():
    pass


if __name__ == '__main__':
    main()
