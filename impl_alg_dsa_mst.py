from GLOBALS import *
from impl_selcet_pos import select_pos
from impl_run_alg_once import run_alg_once


def run_alg_dsa_mst(iteration, pos_list, targets_list, agents_list, objects_dict):
    for agent in agents_list:
        # collect positions of neighbours

        for nei_agent in agents_list:
            pass

        # create targets with curr_req

        # get new_pos
        new_pos = select_pos(agent, targets_list, pos_list)

        # replacement decision

        agent.pos = new_pos


if __name__ == '__main__':
    LIFESPAN = 120
    SIDE_SIZE = 50
    run_alg_once(alg_func=run_alg_dsa_mst, alg_name='DST_MST', side_size=SIDE_SIZE, lifespan=LIFESPAN)
