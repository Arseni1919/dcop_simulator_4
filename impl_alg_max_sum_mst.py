from functions import *
from impl_run_alg_once import run_alg_once


def run_alg_max_sum_mst(iteration, pos_list, targets_list, agents_list, objects_dict):
    for agent in agents_list:
        agent.pos = get_random_pos(agent, objects_dict)


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_max_sum_mst, alg_name='max_sum_mst', side_size=SIDE_SIZE, lifespan=LIFESPAN)