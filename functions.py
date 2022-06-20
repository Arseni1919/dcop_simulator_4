from GLOBALS import *


def get_closest_pos(to_pos, from_pos, objects_dict):
    pos_dict = {}
    for pos_name in from_pos.neighbours:
        pos_node = objects_dict[pos_name]
        pos_dict[pos_node] = distance_nodes(to_pos, pos_node)
    min_pos = min(pos_dict, key=pos_dict.get)
    return min_pos


def calc_target_remained_cov(agents_list, target, up_value):
    sum_of_creds = 0
    for agent in agents_list:
        dist = distance_nodes(target.pos, agent.pos)
        if dist < agent.sr:
            sum_of_creds += agent.cred
    target_remained_cov = max(0, up_value * target.req - sum_of_creds)
    return target_remained_cov


def get_coverage_value(targets_list, agents_list, i_time):
    total_remained_cov = 0
    for target in targets_list:
        up_value = target.up_values[i_time]
        if up_value > 0:
            target_remained_cov = calc_target_remained_cov(agents_list, target, up_value)
            total_remained_cov += target_remained_cov

    return total_remained_cov


def get_collisions_value(targets_list, agents_list, i_time):

    # vertex collisions
    vertex_collisions = 0
    for agent_1 in agents_list:
        for agent_2 in agents_list:
            if agent_1.name != agent_2.name:
                if agent_1.pos.name == agent_2.pos.name:
                    vertex_collisions += 1
    vertex_collisions /= 2

    # edge collisions
    edge_collisions = 0

    return vertex_collisions + edge_collisions


def distance_nodes(pos1, pos2):
    return math.sqrt(math.pow(pos1.x - pos2.x, 2) + math.pow(pos1.y - pos2.y, 2))


def get_temp_req(agents_list, targets_list, iteration):
    temp_req = []
    for target in targets_list:
        up_value = target.up_values[iteration]
        if up_value > 0:
            # create a copy
            copied_target = copy.deepcopy(target)
            copied_target.req = copied_target.req * up_value

            # get cov out of req
            for agent in agents_list:
                if distance_nodes(copied_target.pos, agent.pos) <= agent.sr:
                    copied_target.req = max(0, copied_target.req - agent.sr)

            # add to a new list
            temp_req.append(copied_target)

    return temp_req


def get_random_pos(agent, objects_dict):
    next_pos_list = [pos_name for pos_name in agent.pos.neighbours]
    next_pos_list.append(agent.pos.name)
    rand_choice = objects_dict[random.choice(next_pos_list)]
    return rand_choice


def breakdowns_correction(agents_list, agents_new_pos):

    for agent_1 in agents_list:
        good_to_go = True
        for agent_2 in agents_list:
            if agent_1.name != agent_2.name:
                # next pos
                if agents_new_pos[agent_1.name].name == agents_new_pos[agent_2.name].name:
                    good_to_go = False
                    break
                # current pos
                if agents_new_pos[agent_1.name].name == agent_2.pos.name:
                    good_to_go = False
                    break
        if good_to_go:
            agent_1.pos = agents_new_pos[agent_1.name]

    # check
    # for agent_1 in agents_list:
    #     for agent_2 in agents_list:
    #         if agent_1.name != agent_2.name:
    #             if agent_1.pos.name == agent_2.pos.name:
    #                 print('!!! COL')


def main():
    pass


if __name__ == '__main__':
    main()
