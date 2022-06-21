from functions import *
from impl_run_alg_once import run_alg_once


class VarNode:
    def __init__(self, agent, objects_dict, small_iterations):
        self.node = agent
        self.objects_dict = objects_dict
        self.messages = {s_iter: {} for s_iter in range(small_iterations)}
        self.nei_list = []

    def send_messages(self):
        pass

    def choose_assignment(self):
        self.node.pos = get_random_pos(self.node, self.objects_dict)


class FuncTargetNode:
    def __init__(self, target, small_iterations):
        self.node = target
        self.messages = {s_iter: {} for s_iter in range(small_iterations)}
        self.nei_list = []

    def send_messages(self):
        pass


class FuncPosNode:
    def __init__(self, pos, small_iterations):
        self.node = pos
        self.messages = {s_iter: {} for s_iter in range(small_iterations)}
        self.nei_list = []

    def send_messages(self):
        pass


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


def create_t_function_nodes(agents_list, temp_req, pos_list, small_iterations):
    function_nodes = []
    for target in temp_req:
        func_target_node = FuncTargetNode(target, small_iterations)
        function_nodes.append(func_target_node)
    return function_nodes


def create_variable_nodes(agents_list, temp_req, pos_list, objects_dict, small_iterations):
    variable_nodes = []
    for agent in agents_list:
        variable_nodes.append(VarNode(agent, objects_dict, small_iterations))
    return variable_nodes


def set_neighbours(function_nodes, variable_nodes):
    for f_node in function_nodes:
        for v_node in variable_nodes:
            dist = distance_nodes(f_node.node.pos, v_node.node.pos)
            if dist <= v_node.node.sr + v_node.node.mr:
                f_node.nei_list.append(v_node)
                v_node.nei_list.append(f_node)


def run_alg_max_sum_mst(iteration, pos_list, targets_list, agents_list, objects_dict):
    # parameters
    SMALL_ITERATIONS = 10

    # build factor graph
    temp_req = get_temp_req([], targets_list, iteration)
    function_nodes = create_t_function_nodes(agents_list, temp_req, pos_list, SMALL_ITERATIONS)
    variable_nodes = create_variable_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    set_neighbours(function_nodes, variable_nodes)

    # small iterations
    for small_iteration in range(SMALL_ITERATIONS):

        # function nodes
        for f_node in function_nodes:
            f_node.send_messages()

        # variable nodes
        for v_node in variable_nodes:
            v_node.send_messages()

    # choose next position
    for v_node in variable_nodes:
        v_node.choose_assignment()


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_max_sum_mst, alg_name='max_sum_mst', side_size=SIDE_SIZE, lifespan=LIFESPAN)
