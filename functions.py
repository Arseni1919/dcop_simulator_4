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
                    if not agent_1.broken_bool:
                        vertex_collisions += 1
                    elif agent_1.broken_time == i_time:
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


def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)


def flatten_message(message, to_flatten=True):
    if to_flatten:
        min_value = min(message.values())
        return {pos_i: value - min_value for pos_i, value in message.items()}
    return message


def zeros_message(ms_node, default_value=0.0):
    return {pos_i: default_value for pos_i in ms_node.node.pos.neighbours}


def cover_target(target, robots_set):
    cumulative_cov = sum([robot.node.cred for robot in robots_set])
    return cumulative_cov > target.node.req


def select_FMR_nei(target):
    total_set = []
    SR_set = []
    rest_set = []

    for robot in target.nei_list:
        dist = distance_nodes(robot.node.pos, target.node.pos)

        if dist <= robot.node.sr + robot.node.mr:
            total_set.append(robot)
            if dist <= robot.node.sr:
                SR_set.append(robot)
            else:
                rest_set.append(robot)

    while cover_target(target, total_set):
        def get_degree(node):
            targets_nearby = list(filter(lambda x: 'target' in x.node.name, node.nei_list))
            return len(targets_nearby)
        max_degree = max([get_degree(x) for x in rest_set], default=0)
        min_degree = min([get_degree(x) for x in SR_set], default=0)
        if len(rest_set) > 0:
            selected_to_remove = list(filter(lambda x: get_degree(x) == max_degree, rest_set))[0]
            rest_set.remove(selected_to_remove)
        else:
            selected_to_remove = list(filter(lambda x: get_degree(x) == min_degree, SR_set))[0]
            SR_set.remove(selected_to_remove)

        temp_total_set = total_set[:]
        temp_total_set.remove(selected_to_remove)
        if not cover_target(target, temp_total_set):
            break
        total_set.remove(selected_to_remove)
    # return total_set

    total_set.sort(key=lambda x: x.node.cred, reverse=True)
    return_set = []
    for robot in total_set:
        if not cover_target(target, return_set):
            return_set.append(robot)
    if len(total_set) > len(return_set):
        pass
    return return_set


def execute_breakdowns(iteration, agents_list):
    # broken no moving
    for agent_1 in agents_list:
        if agent_1.broken_bool:
            agent_1.pos = agent_1.broken_pos

    # breakdowns
    for agent_1 in agents_list:
        for agent_2 in agents_list:
            if agent_1.name != agent_2.name:
                if agent_1.pos.name == agent_2.pos.name:
                    agent_1.get_broken(agent_1.pos, iteration)
                    agent_2.get_broken(agent_2.pos, iteration)


def save_results(algs_to_compare, n_problems, n_iters, big_cov_dict, big_col_dict):
    # the json file where the output must be stored
    for alg_name in algs_to_compare:
        big_cov_dict[alg_name] = big_cov_dict[alg_name].tolist()
        big_col_dict[alg_name] = big_col_dict[alg_name].tolist()
    curr_dt = datetime.now()
    time_adding = f"{curr_dt.year}-{curr_dt.month}-{curr_dt.day}-{curr_dt.hour}-{curr_dt.minute}"
    out_file = open(f"data/{time_adding}_problems_{n_problems}__iters_{n_iters}_cov.json", "w")
    json.dump(big_cov_dict, out_file, indent=2)
    out_file.close()

    out_file = open(f"data/problems_{n_problems}__iters_{n_iters}_col.json", "w")
    json.dump(big_col_dict, out_file, indent=2)
    out_file.close()

    # # Opening JSON file
    # f = open('data.json')
    # # returns JSON object as
    # # a dictionary
    # data = json.load(f)
    # # Iterating through the json
    # # list
    # for i in data['emp_details']:
    #     print(i)
    # # Closing file
    # f.close()

def main():
    pass


if __name__ == '__main__':
    main()
