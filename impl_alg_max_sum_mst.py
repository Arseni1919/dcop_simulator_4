from functions import *
from impl_run_alg_once import run_alg_once


class VarNode:
    def __init__(self, agent, objects_dict, small_iterations):
        self.node = agent
        self.objects_dict = objects_dict
        self.messages = {s_iter: {} for s_iter in range(small_iterations)}
        self.nei_list = []

    def send_messages(self, s_iter):
        if s_iter > 0:
            for func_nei in self.nei_list:
                message = zeros_message(self)
                for other_nei in self.nei_list:
                    if other_nei.node.name != func_nei.node.name:
                        past_message = self.messages[s_iter - 1][func_nei.node.name]
                        for d in self.node.pos.neighbours:
                            message[d] += past_message[d]
                message = flatten_message(message)
                func_nei.messages[s_iter][self.node.name] = message

    def choose_assignment(self, small_iterations):
        if len(self.nei_list) > 0:
            message = zeros_message(self)
            max_value = 0.0
            for func_nei in self.nei_list:
                past_message = self.messages[small_iterations - 1][func_nei.node.name]
                for d in self.node.pos.neighbours:
                    message[d] += past_message[d]
                    if message[d] >= max_value:
                        max_value = message[d]

            max_poses = [k for k, v in message.items() if v == max_value]
            self.node.pos = self.objects_dict[random.choice(max_poses)]
        else:
            self.node.pos = get_random_pos(self.node, self.objects_dict)


class FuncTargetNode:
    def __init__(self, target, small_iterations, objects_dict):
        self.node = target
        self.messages = {s_iter: {} for s_iter in range(small_iterations)}
        self.nei_list = []
        self.objects_dict = objects_dict

    def _create_list_of_domains(self, send_to_var_nei):
        list_of_other_domains = []
        list_of_other_nei = []
        for nei in self.nei_list:
            if nei.node.name != send_to_var_nei.node.name:
                list_of_other_domains.append(nei.node.pos.neighbours)
                list_of_other_nei.append(nei)
        return list_of_other_domains, list_of_other_nei

    def func(self, v_node, pos_i, comb_of_other_nei_pos, list_of_other_nei):
        # comb = {"name_of_nei": binary(0,1), ... } | 1 - in, 0 - out
        coverage = 0

        if distance_nodes(self.objects_dict[pos_i], self.node.pos) < v_node.node.sr:
            coverage += v_node.node.cred

        for pos_of_nei, nei in zip(comb_of_other_nei_pos, list_of_other_nei):
            if distance_nodes(self.objects_dict[pos_of_nei], self.node.pos) < nei.node.sr:
                coverage += nei.node.cred

        return min(coverage, self.node.req)

    def _prev_iter_brings(self, iteration, comb_of_other_nei_pos, list_of_other_nei):
        if iteration == 0:
            return 0
        prev_iteration_brings = 0
        for other_nei_pos, other_nei in zip(comb_of_other_nei_pos, list_of_other_nei):
            # iteration -> name -> position -> value
            prev_iteration_brings += self.messages[iteration - 1][other_nei.node.name][other_nei_pos]
        return prev_iteration_brings

    def send_messages(self, s_iter):
        MINUS_INF = -70000
        for v_node in self.nei_list:
            message = zeros_message(v_node, default_value=MINUS_INF)
            list_of_other_domains, list_of_other_nei = self._create_list_of_domains(v_node)
            comb_of_other_nei_pos_list = list(itertools.product(*list_of_other_domains))
            for comb_of_other_nei_pos in comb_of_other_nei_pos_list:
                for pos_i in v_node.node.pos.neighbours:
                    message[pos_i] = max(
                        message[pos_i],

                        (
                                self.func(v_node, pos_i, comb_of_other_nei_pos, list_of_other_nei) +
                                self._prev_iter_brings(s_iter, comb_of_other_nei_pos, list_of_other_nei)
                        )
                    )

            message = flatten_message(message)
            v_node.messages[s_iter][self.node.name] = message


class FuncPosNode:
    def __init__(self, pos, small_iterations):
        self.node = pos
        self.messages = {s_iter: {} for s_iter in range(small_iterations)}
        self.nei_list = []

    def send_messages(self):
        pass


def create_t_function_nodes(agents_list, temp_req, pos_list, objects_dict, small_iterations):
    function_nodes = []
    for target in temp_req:
        func_target_node = FuncTargetNode(target, small_iterations,  objects_dict)
        function_nodes.append(func_target_node)
    return function_nodes


def create_variable_nodes(agents_list, temp_req, pos_list, objects_dict, small_iterations):
    variable_nodes = []
    for agent in agents_list:
        variable_nodes.append(VarNode(agent, objects_dict, small_iterations))
    return variable_nodes


def set_neighbours(function_nodes, variable_nodes, small_iterations):
    for f_node in function_nodes:
        for v_node in variable_nodes:
            dist = distance_nodes(f_node.node.pos, v_node.node.pos)
            if dist <= v_node.node.sr + v_node.node.mr:
                f_node.nei_list.append(v_node)

    # FMR exclusion
    for target in function_nodes:
        new_nei_list = select_FMR_nei(target)
        # if len(new_nei_list) < len(target.nei_list):
        #     print(f'original len of nei list vs FMR len: {len(target.nei_list)} -> {len(new_nei_list)}')
        target.nei_list = new_nei_list

    for f_node in function_nodes:

        # add func node nei to var nodes
        for v_node in f_node.nei_list:
            v_node.nei_list.append(f_node)

            # update message dicts of both
            for s_iter in range(small_iterations):
                v_node.messages[s_iter][f_node.node.name] = zeros_message(v_node)
                f_node.messages[s_iter][v_node.node.name] = zeros_message(v_node)


def run_alg_max_sum_mst(iteration, pos_list, targets_list, agents_list, objects_dict):
    # parameters
    SMALL_ITERATIONS = 10

    # build factor graph
    temp_req = get_temp_req([], targets_list, iteration)
    function_nodes = create_t_function_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    variable_nodes = create_variable_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    set_neighbours(function_nodes, variable_nodes, SMALL_ITERATIONS)

    # small iterations
    for s_iter in range(SMALL_ITERATIONS):

        # function nodes
        for f_node in function_nodes:
            f_node.send_messages(s_iter=s_iter)

        # variable nodes
        for v_node in variable_nodes:
            v_node.send_messages(s_iter=s_iter)

    # choose next position
    for v_node in variable_nodes:
        v_node.choose_assignment(SMALL_ITERATIONS)


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30

    # SEED
    set_seed(seed=12)

    run_alg_once(
        alg_func=run_alg_max_sum_mst,
        alg_name='max_sum_mst',
        side_size=SIDE_SIZE,
        lifespan=LIFESPAN,
        # const_app=True
    )
