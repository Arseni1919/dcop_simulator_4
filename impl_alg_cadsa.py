from impl_alg_dsa_mst import *


def run_alg_cadsa(iteration, pos_list, targets_list, agents_list, objects_dict):
    # FIRST STAGE (as in dsa_mst)
    agents_new_pos = {}
    for agent in agents_list:
        chosen_pos = agent.pos
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
                chosen_pos = new_pos
        else:
            chosen_pos = get_random_pos(agent, objects_dict)

        agents_new_pos[agent.name] = chosen_pos

    # SECOND STAGE
    breakdowns_correction(agents_list, agents_new_pos)


if __name__ == '__main__':
    LIFESPAN = 120
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_cadsa, alg_name='DST_MST', side_size=SIDE_SIZE, lifespan=LIFESPAN)
