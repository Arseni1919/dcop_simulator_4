import numpy as np

from plot_functions import *
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *
from impl_algs_dict import algs_dict
from impl_compare_algs import init_start_positions


def compare_algs_in_scale():
    plotter = PlotField(side_size=SIDE_SIZE, life_plot=LIFE_PLOT)
    big_cov_dict = {alg_name: np.zeros((LIFESPAN, N_PROBLEMS)) for alg_name in algs_to_compare}
    big_col_dict = {alg_name: np.zeros((LIFESPAN, N_PROBLEMS)) for alg_name in algs_to_compare}
    # problems
    for i_problem in range(N_PROBLEMS):

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
            rand_pos_nei=RAND_POS_NEI
        )
        # clear online graphs
        plotter.clean_trackers()

        # algorithms
        for i_alg, alg_name in enumerate(algs_to_compare):

            alg_func = algs_dict[alg_name]
            init_start_positions(agents_list)

            # iterations
            for i_iter in range(LIFESPAN):
                print(f'\rproblem: {i_problem + 1}/{N_PROBLEMS}, alg: "{alg_name}" {i_alg + 1}/{len(algs_to_compare)}, iteration: {i_iter + 1}/{LIFESPAN}', end='')
                alg_func(i_iter, pos_list, targets_list, agents_list, objects_dict)

                # metrics
                coverage_value = get_coverage_value(targets_list, agents_list, i_time=i_iter)
                big_cov_dict[alg_name][i_iter][i_problem] = coverage_value
                collisions_value = get_collisions_value(targets_list, agents_list, i_time=i_iter)
                big_col_dict[alg_name][i_iter][i_problem] = collisions_value
                # plots
                plotter.update_trackers(alg_name, coverage_value, collisions_value)

                # stop on collision
                # if alg_name == 'cams' and collisions_value > 0:
                #     plotter.plot_field(i_iter, pos_list, targets_list, agents_list, lifespan=LIFESPAN)
                #     input()

                # after inter and metrics
                update_prev_pos(agents_list)

    plotter.show()

    # save_results(algs_to_compare, N_PROBLEMS, LIFESPAN, comment, big_cov_dict, big_col_dict)
    plot_big_cov_graph(big_cov_dict, algs_to_compare, LIFESPAN)
    plot_big_col_graph(big_col_dict, algs_to_compare, LIFESPAN)


if __name__ == '__main__':
    # LIFESPAN = 120
    LIFESPAN = 80
    # LIFESPAN = 15
    N_PROBLEMS = 20
    # N_PROBLEMS = 5
    # N_TARGETS = 20
    N_TARGETS = 3
    # N_AGENTS = 30
    N_AGENTS = 8
    DECAY_RATE = 3
    MIN_LIFE = 20
    # MIN_LIFE = 10
    MAX_LIFE = 50
    TARGETS_APART = True
    # TARGETS_APART = False
    CONSTANT_APPEARANCE = False
    # CONSTANT_APPEARANCE = True
    # SIDE_SIZE = 50
    SIDE_SIZE = 25
    RAND_POS_NEI = True
    # RAND_POS_NEI = False
    comment = 'static' if CONSTANT_APPEARANCE else 'dynamic'
    comment += '_RAND_POS_NEI' if RAND_POS_NEI else '_GRID'
    # SR = 3
    SR = 2
    LIFE_PLOT = True
    # LIFE_PLOT = False

    algs_to_compare = [
        'cams',

        'max_sum_mst - breakdowns',
        'max_sum_mst',
        'dssa',
        'ca_select_pos',
        'cadsa',
        'dsa_mst',
        'random',

        # 'hard_constrained_cams',
        # 'hard_constrained_ms',
        # 'greedy_select_pos',
        # 'greedy',
    ]

    # SEED
    # set_seed(seed=12)

    compare_algs_in_scale()
