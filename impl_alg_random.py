from functions import *
from impl_run_alg_once import run_alg_once


def run_alg_random(iteration, pos_list, targets_list, agents_list, objects_dict):
    for agent in agents_list:
        agent.pos = get_random_pos(agent, objects_dict)


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_random, alg_name='random', side_size=SIDE_SIZE, lifespan=LIFESPAN)
