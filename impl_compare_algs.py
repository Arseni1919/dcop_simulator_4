from plot_functions import *
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *
from impl_alg_random import run_alg_random
from impl_alg_greedy import run_alg_greedy
from impl_alg_dsa_mst import run_alg_dsa_mst
from impl_alg_greedy_select_pos import run_alg_greedy_select_pos
from impl_alg_cadsa import run_alg_cadsa
from impl_alg_ca_greedy_select_pos import run_alg_ca_greedy_select_pos
from impl_alg_dssa import run_alg_dssa
from impl_alg_ms_mst import run_alg_max_sum_mst
from impl_alg_cams import run_alg_cams
from impl_alg_ms_mst_breakdowns import run_max_sum_mst_breakdowns


def init_start_positions(agents_list):
    for agent in agents_list:
        agent.pos = agent.start_pos
        agent.reset_broken()


def compare_algs():

    # problems
    plotter = PlotField(side_size=SIDE_SIZE)
    pos_list, targets_list, agents_list, objects_dict = create_dynamic_dcop_setting(
        lifespan=LIFESPAN,
        n_agents=N_AGENTS,
        n_targets=N_TARGETS,
        agent_sr=SR,
        target_decay_rate=DECAY_RATE,
        target_min_life=MIN_LIFE,
        target_max_life=MAX_LIFE,
        side_size=SIDE_SIZE,
        targets_apart=TARGETS_APART,
        const_app=CONSTANT_APPEARANCE,
    )

    # algorithms
    for alg_name in algs_to_compare:

        alg_func = algs_dict[alg_name]
        init_start_positions(agents_list)

        # iterations
        for i in range(LIFESPAN):
            print(f'\ralg: {alg_name}, iteration: {i}', end='')
            alg_func(i, pos_list, targets_list, agents_list, objects_dict)

            # metrics
            coverage_value = get_coverage_value(targets_list, agents_list, i_time=i)
            collisions_value = get_collisions_value(targets_list, agents_list, i_time=i)

            # plots
            plotter.update_trackers(alg_name, coverage_value, collisions_value)
            plotter.plot_field(i, pos_list, targets_list, agents_list, lifespan=LIFESPAN)

    plotter.show()


if __name__ == '__main__':
    LIFESPAN = 120
    N_TARGETS = 20
    N_AGENTS = 20
    DECAY_RATE = 3
    MIN_LIFE = 40
    MAX_LIFE = 50
    TARGETS_APART = True
    CONSTANT_APPEARANCE = False
    SIDE_SIZE = 40
    SR = 3

    algs_dict = {
        'random': run_alg_random,
        'greedy': run_alg_greedy,
        'dsa_mst': run_alg_dsa_mst,
        'greedy_select_pos': run_alg_greedy_select_pos,
        'ca_select_pos': run_alg_ca_greedy_select_pos,
        'cadsa': run_alg_cadsa,
        'dssa': run_alg_dssa,
        'max_sum_mst': run_alg_max_sum_mst,
        'max_sum_mst \n with breakdowns': run_max_sum_mst_breakdowns,
        'cams': run_alg_cams,
    }

    algs_to_compare = [
        'max_sum_mst \n with breakdowns',
        'cams',
        'max_sum_mst',
        'dssa',
        'ca_select_pos',
        'cadsa',
        'dsa_mst',
        'greedy_select_pos',
        # 'greedy',
        'random'
    ]

    # SEED
    # set_seed(seed=12)

    compare_algs()
