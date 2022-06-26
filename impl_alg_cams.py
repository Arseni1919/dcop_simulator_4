from functions import *
from impl_run_alg_once import run_alg_once
from impl_alg_max_sum_mst import create_variable_nodes, create_t_function_nodes, set_target_neighbours


class FuncPosNode:
    def __init__(self, pos, small_iterations, objects_dict):
        self.node = pos
        self.messages = {s_iter: {} for s_iter in range(small_iterations)}
        self.nei_list = []
        self.objects_dict = objects_dict
        self.weights = {}
        self.inf = -70000

    def _create_list_of_domains(self, send_to_var_nei):
        list_of_other_domains = []
        list_of_other_nei = []
        for nei in self.nei_list:
            if nei.node.name != send_to_var_nei.node.name:
                list_of_other_domains.append(nei.node.pos.neighbours)
                list_of_other_nei.append(nei)
        return list_of_other_domains, list_of_other_nei

    def func(self, v_node, pos_i, comb_of_other_nei_pos, list_of_other_nei):
        overall_comb = [pos_i]
        overall_comb.extend(comb_of_other_nei_pos)
        self_name_in_comb = [pos_name for pos_name in overall_comb if pos_name == self.node.name]
        len_of_self_name_in_comb = len(self_name_in_comb)
        if len_of_self_name_in_comb > 1:
            return self.inf
        elif len_of_self_name_in_comb == 0:
            return 0
        else:
            overall_comb_dict = {pos_i: v_node}
            overall_comb_dict.update({nei_name: nei_node for nei_name, nei_node in zip(comb_of_other_nei_pos, list_of_other_nei) })
            return_value = self.weights[overall_comb_dict[self.node.name].node.name]
            return return_value

    def _prev_iter_brings(self, iteration, comb_of_other_nei_pos, list_of_other_nei):
        if iteration == 0:
            return 0
        prev_iteration_brings = 0
        for other_nei_pos, other_nei in zip(comb_of_other_nei_pos, list_of_other_nei):
            # iteration -> name -> position -> value
            prev_iteration_brings += self.messages[iteration - 1][other_nei.node.name][other_nei_pos]
        return prev_iteration_brings

    def send_messages(self, s_iter):

        for v_node in self.nei_list:
            message = zeros_message(v_node, default_value=self.inf)
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

    def dust_weights(self):
        for nei_robot in self.nei_list:
            self.weights[nei_robot.node.name] = random.uniform(1e-10, 1e-5)


def create_p_function_nodes(agents_list, temp_req, pos_list, objects_dict, small_iterations):
    func_p_nodes = []
    for pos in pos_list:
        func_p_node = FuncPosNode(pos, small_iterations,  objects_dict)
        func_p_nodes.append(func_p_node)
    return func_p_nodes


def set_pos_neighbours(func_p_nodes, variable_nodes, small_iterations):
    # POS NODES
    func_p_dict = {func_p_node.node.name: func_p_node for func_p_node in func_p_nodes}
    for v_node in variable_nodes:
        for nei_name in v_node.node.pos.neighbours:
            p_nei = func_p_dict[nei_name]
            p_nei.nei_list.append(v_node)
            v_node.nei_list.append(p_nei)

            # update message dicts of both
            for s_iter in range(small_iterations):
                v_node.messages[s_iter][p_nei.node.name] = zeros_message(v_node)
                p_nei.messages[s_iter][v_node.node.name] = zeros_message(v_node)

    # dust weights
    _ = [func_p.dust_weights() for func_p in func_p_nodes]


def run_alg_cams(iteration, pos_list, targets_list, agents_list, objects_dict):
    # parameters
    SMALL_ITERATIONS = 10

    # build factor graph
    temp_req = get_temp_req([], targets_list, iteration)
    func_t_nodes = create_t_function_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    func_p_nodes = create_p_function_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    variable_nodes = create_variable_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    set_target_neighbours(func_t_nodes, variable_nodes, SMALL_ITERATIONS)
    set_pos_neighbours(func_p_nodes, variable_nodes, SMALL_ITERATIONS)

    # small iterations
    for s_iter in range(SMALL_ITERATIONS):

        # func target nodes
        for f_node in func_t_nodes:
            f_node.send_messages(s_iter=s_iter)

        # func pos nodes
        for f_node in func_p_nodes:
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
        alg_func=run_alg_cams,
        alg_name='cams',
        side_size=SIDE_SIZE,
        lifespan=LIFESPAN,
        # const_app=True
    )