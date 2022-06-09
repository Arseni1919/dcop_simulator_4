from plot_functions import *
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *


def run_greedy_2_alg(iteration, pos_list, targets_list, agents_list, objects_dict):
    active_t_list = list(filter(lambda x: x.up_values[iteration] > 0, targets_list))

    # targets send messages
    remained_cov_dict = {}
    for target in active_t_list:
        up_value = target.up_values[iteration]
        target_remained_cov = calc_target_remained_cov(agents_list, target, up_value)
        remained_cov_dict[target.name] = target_remained_cov

    # agents decide
    for agent in agents_list:
        if len(active_t_list) > 0 and random.random() < 0.5:
            agent_target_dict = {}
            for target in active_t_list:
                agent_target_dict[target] = max(0, remained_cov_dict[target.name] - agent.cred)
            max_cov_target = max(agent_target_dict, key=agent_target_dict.get)

            # get closest pos
            choice = get_closest_pos(to_pos=max_cov_target.pos, from_pos=agent.pos, objects_dict=objects_dict)
        else:
            choice = objects_dict[random.choice(agent.pos.neighbours)]
        agent.pos = choice


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
        run_greedy_2_alg(i, pos_list, targets_list, agents_list, objects_dict)
        coverage_value = get_coverage_value(targets_list, agents_list, i_time=i)
        plotter.update_tracker('greedy_2', coverage_value)
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
