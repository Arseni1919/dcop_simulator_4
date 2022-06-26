from functions import *
from impl_run_alg_once import run_alg_once
from impl_alg_ms_mst import run_alg_max_sum_mst


def run_max_sum_mst_breakdowns(iteration, pos_list, targets_list, agents_list, objects_dict):
    run_alg_max_sum_mst(iteration, pos_list, targets_list, agents_list, objects_dict)
    execute_breakdowns(iteration, agents_list)


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30

    # SEED
    set_seed(seed=12)

    run_alg_once(
        alg_func=run_max_sum_mst_breakdowns,
        alg_name='run_max_sum_mst_breakdowns',
        side_size=SIDE_SIZE,
        lifespan=LIFESPAN,
        # const_app=True
    )