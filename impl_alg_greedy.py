from plot_functions import *
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *
from impl_run_alg_once import run_alg_once


def run_alg_greedy(iteration, pos_list, targets_list, agents_list, objects_dict):
    active_t_list = list(filter(lambda x: x.up_values[iteration] > 0, targets_list))
    for agent in agents_list:
        pos_name_value_dict = {}
        for pos_name in agent.pos.neighbours:
            pos_node = objects_dict[pos_name]
            nearby_t_list = list(filter(lambda x: distance_nodes(x.pos, pos_node) < agent.sr, active_t_list))
            if len(nearby_t_list) == 0:
                pos_name_value_dict[pos_name] = 0
            else:
                cov_value = sum([x.req for x in nearby_t_list])
                pos_name_value_dict[pos_name] = cov_value

        if max(list(pos_name_value_dict.values())) == 0:
            choice = objects_dict[random.choice(agent.pos.neighbours)]
        else:
            max_pos_name = max(pos_name_value_dict, key=pos_name_value_dict.get)
            choice = objects_dict[max_pos_name]

        agent.pos = choice


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 50
    run_alg_once(alg_func=run_alg_greedy, alg_name='greedy', side_size=SIDE_SIZE, lifespan=LIFESPAN)


# plotter = PlotField(side_size=SIDE_SIZE)
#     pos_list, targets_list, agents_list, objects_dict = create_dynamic_dcop_setting(
#         lifespan=LIFESPAN,
#         n_agents=N_AGENTS,
#         n_targets=N_TARGETS,
#         agent_sr=SR,
#         target_decay_rate=DECAY_RATE,
#         target_min_life=MIN_LIFE,
#         target_max_life=MAX_LIFE,
#         side_size=SIDE_SIZE
#     )
#     for i in range(LIFESPAN):
#         print(f'\riteration: {i}', end='')
#         run_alg_greedy(i, pos_list, targets_list, agents_list, objects_dict)
#         coverage_value = get_coverage_value(targets_list, agents_list, i_time=i)
#         plotter.update_tracker('greedy', coverage_value)
#         plotter.plot_field(i, pos_list, targets_list, agents_list, lifespan=LIFESPAN)