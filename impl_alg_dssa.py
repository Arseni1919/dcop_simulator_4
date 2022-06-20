from impl_alg_dsa_mst import *


def not_accept_others_new_pos(agent, agents_list, agents_new_pos):
    my_next_pos_name = agents_new_pos[agent.name].name
    for agent_2 in agents_list:
        if agent_2.name != agent.name:
            if agents_new_pos[agent_2.name].name == my_next_pos_name:
                return True
    return False


def set_first_intention(iteration, pos_list, targets_list, agents_list, objects_dict, agents_new_pos):
    for agent in agents_list:
        nei_agents = get_nei_agents(agent, agents_list)
        temp_req = get_temp_req(nei_agents, targets_list, iteration)
        if len(temp_req) > 0:
            new_pos = select_pos(agent, temp_req, pos_list)
        else:
            new_pos = get_random_pos(agent, objects_dict)
        agents_new_pos[agent.name] = new_pos


def set_diff_intention(agent, agents_list, targets_list, pos_list, iteration, objects_dict, agents_new_pos):
    nei_agents = get_nei_agents(agent, agents_list)
    temp_req = get_temp_req(nei_agents, targets_list, iteration)
    if len(temp_req) > 0:
        robot_pos_name_set = [pos_name for pos_name in agent.pos.neighbours]
        robot_pos_name_set.append(agent.pos.name)
        robot_pos_name_set.remove(agents_new_pos[agent.name].name)
        new_pos = select_pos(agent, temp_req, pos_list, robot_pos_name_set=robot_pos_name_set)
    else:
        new_pos = get_random_pos(agent, objects_dict)
    agents_new_pos[agent.name] = new_pos


def run_alg_dssa(iteration, pos_list, targets_list, agents_list, objects_dict):
    # FIRST STAGE (as in dsa_mst)
    agents_new_pos = {agent.name: agent.pos for agent in agents_list}
    set_first_intention(iteration, pos_list, targets_list, agents_list, objects_dict, agents_new_pos)

    need_to_talk = True
    tries = 0
    while need_to_talk and tries < 20:
        tries += 1

        need_to_talk = False
        for agent in agents_list:
            if not_accept_others_new_pos(agent, agents_list, agents_new_pos):
                need_to_talk = True
                # replacement decision
                nei_agents = get_nei_agents(agent, agents_list)
                temp_req = get_temp_req(nei_agents, targets_list, iteration)
                replacement_decision = get_replacement_decision(agent, agents_new_pos[agent.name], temp_req)
                if not replacement_decision:
                    set_diff_intention(agent, agents_list, targets_list, pos_list, iteration, objects_dict, agents_new_pos)

    # SECOND STAGE
    # print(f', tries: {tries}', end='')
    for agent in agents_list:
        agent.pos = agents_new_pos[agent.name]
    # breakdowns_correction(agents_list, agents_new_pos)

    # check
    for agent_1 in agents_list:
        for agent_2 in agents_list:
            if agent_1.name != agent_2.name:
                if agent_1.pos.name == agent_2.pos.name:
                    print('!!! COL')


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_dssa, alg_name='greedy', side_size=SIDE_SIZE, lifespan=LIFESPAN)