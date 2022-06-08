from GLOBALS import *


class PosNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = f'{x}_{y}'
        self.neighbours = []


class TargetNode:
    def __init__(self, i, decay_rate=3, min_life=10, max_life=30, lifespan=100, pos=None):
        self.num = i
        self.name = f'target_{i}'
        self.decay_rate = decay_rate
        self.min_life = min_life
        self.max_life = max_life
        self.lifespan = lifespan
        self.pos = pos


class AgentNode:
    def __init__(self, i, sr=10, pos=None):
        self.num = i
        self.name = f'agent_{i}'
        self.sr = sr
        self.pos = pos


def main():
    pass


if __name__ == '__main__':
    main()
