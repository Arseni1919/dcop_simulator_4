from functions import *
from impl_run_alg_once import run_alg_once


def cover_target(target, robots_set):
    cumulative_cov = sum([robot.cred for robot in robots_set])
    return cumulative_cov > target.req


def select_FMR_nei(target):
    total_set = []
    SR_set = []
    rest_set = []

    for robot in target.neighbours:
        dist = distance_nodes(robot.pos, target.pos)

        if dist <= robot.sr + robot.mr:
            total_set.append(robot)
            if dist <= robot.sr:
                SR_set.append(robot)
            else:
                rest_set.append(robot)

    while cover_target(target, total_set):
        def get_degree(node):
            targets_nearby = list(filter(lambda x: 'target' in x.name, node.neighbours))
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

    total_set.sort(key=lambda x: x.cred, reverse=True)
    return_set = []
    for robot in total_set:
        if not cover_target(target, return_set):
            return_set.append(robot)
    if len(total_set) > len(return_set):
        pass
    return return_set


def run_alg_max_sum_mst(iteration, pos_list, targets_list, agents_list, objects_dict):
    # parameters
    SMALL_ITERATIONS = 10

    # build factor graph
    temp_req = get_temp_req([], targets_list, iteration)
    # nearby_t_list = list(filter(lambda x: distance_nodes(x.pos, pos_node) < agent.sr, active_t_list))
    pass

    # small iterations
    for small_iteration in range(SMALL_ITERATIONS):

        # function nodes
        pass

        # variable nodes
        pass

    # choose next position
    pass

    for agent in agents_list:
        agent.pos = get_random_pos(agent, objects_dict)


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_max_sum_mst, alg_name='max_sum_mst', side_size=SIDE_SIZE, lifespan=LIFESPAN)
