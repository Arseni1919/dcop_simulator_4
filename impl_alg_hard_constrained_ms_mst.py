from functions import *
from impl_run_alg_once import run_alg_once
from impl_alg_ms_mst import create_variable_nodes, create_t_function_nodes, set_target_neighbours


def run_alg_hard_constrained_ms_mst(iteration, pos_list, targets_list, agents_list, objects_dict):
    # parameters
    SMALL_ITERATIONS = 10

    # build factor graph
    temp_req = get_temp_req([], targets_list, iteration)
    function_nodes = create_t_function_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    variable_nodes = create_variable_nodes(agents_list, temp_req, pos_list, objects_dict, SMALL_ITERATIONS)
    set_target_neighbours(function_nodes, variable_nodes, SMALL_ITERATIONS)

    # small iterations
    for s_iter in range(SMALL_ITERATIONS):

        # function nodes
        for f_node in function_nodes:
            f_node.send_messages(s_iter=s_iter)

        # variable nodes
        for v_node in variable_nodes:
            v_node.send_messages(s_iter=s_iter)

    # choose next position
    agents_new_pos = {}
    for v_node in variable_nodes:
        agents_new_pos[v_node.node.name] = v_node.possible_assignment(SMALL_ITERATIONS)

    breakdowns_correction(agents_list, agents_new_pos)


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30

    # SEED
    set_seed(seed=12)

    run_alg_once(
        alg_func=run_alg_hard_constrained_ms_mst,
        alg_name='hard_constrained_ms_mst',
        side_size=SIDE_SIZE,
        lifespan=LIFESPAN,
        # const_app=True
    )