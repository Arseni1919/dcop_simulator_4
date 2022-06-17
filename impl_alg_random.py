from plot_functions import *
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *


def run_alg_random(iteration, pos_list, targets_list, agents_list, objects_dict):
    for agent in agents_list:
        rand_choice = objects_dict[random.choice(agent.pos.neighbours)]
        agent.pos = rand_choice


def main():
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
    for i in range(LIFESPAN):
        print(f'\riteration: {i}', end='')
        run_alg_random(i, pos_list, targets_list, agents_list, objects_dict)
        coverage_value = get_coverage_value(targets_list, agents_list, i_time=i)
        plotter.update_tracker('random', coverage_value)
        plotter.plot_field(i, pos_list, targets_list, agents_list, lifespan=LIFESPAN)

if __name__ == '__main__':
    LIFESPAN = 100
    N_TARGETS = 30
    N_AGENTS = 30
    DECAY_RATE = 3
    MIN_LIFE = 10
    MAX_LIFE = 50
    SIDE_SIZE = 30
    SR = 5
    main()
