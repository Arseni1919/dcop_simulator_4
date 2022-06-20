import copy

from impl_selcet_pos import select_pos
from impl_run_alg_once import run_alg_once
from functions import *


def get_nei_agents(agent, agents_list):
    nei_agents = []
    for nei_agent in agents_list:
        if distance_nodes(agent.pos, nei_agent.pos) <= agent.sr + nei_agent.sr + agent.mr + nei_agent.mr:
            nei_agents.append(nei_agent)
    return nei_agents


def get_replacement_decision(agent, new_pos, temp_req):
    old_value, new_value = 0, 0

    for target in temp_req:

        # update old_value
        if distance_nodes(target.pos, agent.pos) <= agent.sr:
            old_value += min(target.req, agent.sr)

        # update new value
        if distance_nodes(target.pos, new_pos) <= agent.sr:
            new_value += min(target.req, agent.sr)

    # compare
    if new_value >= old_value:
        # random return
        if random.random() < 0.8:
            return True

    return False


def run_alg_dsa_mst(iteration, pos_list, targets_list, agents_list, objects_dict):
    for agent in agents_list:
        # collect positions of neighbours
        nei_agents = get_nei_agents(agent, agents_list)

        # create targets with curr_req
        temp_req = get_temp_req(nei_agents, targets_list, iteration)

        # get new_pos
        if len(temp_req) > 0:
            new_pos = select_pos(agent, temp_req, pos_list)

            # replacement decision
            replacement_decision = get_replacement_decision(agent, new_pos, temp_req)
            if replacement_decision:
                agent.pos = new_pos
        else:
            agent.pos = get_random_pos(agent, objects_dict)


if __name__ == '__main__':
    LIFESPAN = 120
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_dsa_mst, alg_name='DST_MST', side_size=SIDE_SIZE, lifespan=LIFESPAN)
