import random

from GLOBALS import *


class PosNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = f'{x}_{y}'
        self.neighbours = []
        self.xy_pos = (self.x, self.y)


class TargetNode:
    def __init__(self, i,
                 decay_rate=3, min_life=20, max_life=30, lifespan=100,
                 pos=None, req=100, const=False):
        self.num = i
        self.name = f'target_{i}'
        self.decay_rate = decay_rate
        self.min_life = min_life
        self.max_life = max_life
        self.lifespan = lifespan
        self.pos = pos
        self.req = req
        self.const = const
        self.up_values = []
        self.init()

    def init(self):
        if not self.const:
            # rand_start = random.randint(0, self.lifespan)
            possible_starts = list(range(0, self.lifespan, self.min_life))
            rand_start = random.choice(possible_starts)
            # rand_lifelong = random.randint(self.min_life, self.max_life + 1)
            rand_lifelong = self.min_life * random.randint(1, 4)
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
        else:
            self.up_values = [1.0 for _ in range(self.lifespan)]
        # print(f'{self.name} - up_values: {self.up_values}')


class AgentNode:
    def __init__(self, i, sr=10, pos=None, cred=30):
        self.num = i
        self.name = f'agent_{i}'
        self.sr = sr
        self.mr = 1
        self.start_pos = pos
        self.pos = pos
        self.prev_pos = pos
        self.cred = cred
        self.broken_bool = False
        self.broken_pos = None
        self.broken_time = -1

    def get_broken(self, pos, t):
        if self.broken_time == -1:
            self.broken_bool = True
            self.broken_pos = pos
            self.broken_time = t

    def reset_broken(self):
        self.broken_bool = False
        self.broken_pos = None
        self.broken_time = -1


def main():
    pass


if __name__ == '__main__':
    main()
