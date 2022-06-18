from GLOBALS import *
from impl_selcet_pos import select_pos
from impl_run_alg_once import run_alg_once


def run_alg_greedy_select_pos(iteration, pos_list, targets_list, agents_list, objects_dict):
    for agent in agents_list:
        new_pos = select_pos(agent, targets_list, pos_list)
        agent.pos = new_pos


if __name__ == '__main__':
    LIFESPAN = 120
    SIDE_SIZE = 50
    run_alg_once(
        alg_func=run_alg_greedy_select_pos,
        alg_name='greedy - select_pos',
        side_size=SIDE_SIZE,
        lifespan=LIFESPAN
    )
