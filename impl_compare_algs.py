from plot_functions import *
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *
from impl_alg_random import run_random_alg
from impl_alg_greedy import run_greedy_alg
from impl_alg_greedy_2 import run_greedy_2_alg


def init_start_positions(agents_list):
    for agent in agents_list:
        agent.pos = agent.start_pos


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
        side_size=SIDE_SIZE
    )

    # algorithms
    for alg_name in algs_to_compare:

        alg_func = algs_dict[alg_name]
        init_start_positions(agents_list)

        # iterations
        for i in range(LIFESPAN):
            print(f'\ralg: {alg_name}, iteration: {i}', end='')
            alg_func(i, pos_list, targets_list, agents_list, objects_dict)

            # plots
            coverage_value = get_coverage_value(targets_list, agents_list, i_time=i)
            plotter.update_tracker(alg_name, coverage_value)
            plotter.plot_field(i, pos_list, targets_list, agents_list, lifespan=LIFESPAN)

    plotter.show()


def main():
    compare_algs()


if __name__ == '__main__':
    LIFESPAN = 120
    N_TARGETS = 30
    N_AGENTS = 30
    DECAY_RATE = 3
    MIN_LIFE = 40
    MAX_LIFE = 50
    SIDE_SIZE = 30
    SR = 5

    algs_dict = {
        'random': run_random_alg,
        'greedy': run_greedy_alg,
        'half-greedy': run_greedy_2_alg,
    }
    algs_to_compare = ['half-greedy', 'random', 'greedy']
    main()