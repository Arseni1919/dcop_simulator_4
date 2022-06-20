from functions import *
from impl_selcet_pos import select_pos
from impl_run_alg_once import run_alg_once


def run_alg_ca_greedy_select_pos(iteration, pos_list, targets_list, agents_list, objects_dict):
    agents_new_pos = {}
    for agent in agents_list:
        temp_req = get_temp_req([], targets_list, iteration)
        if len(temp_req) > 0:
            new_pos = select_pos(agent, temp_req, pos_list)
            chosen_pos = new_pos
        else:
            chosen_pos = get_random_pos(agent, objects_dict)

        agents_new_pos[agent.name] = chosen_pos

    breakdowns_correction(agents_list, agents_new_pos)


if __name__ == '__main__':
    LIFESPAN = 120
    SIDE_SIZE = 50
    run_alg_once(
        alg_func=run_alg_ca_greedy_select_pos,
        alg_name='greedy - select_pos',
        side_size=SIDE_SIZE,
        lifespan=LIFESPAN
    )
