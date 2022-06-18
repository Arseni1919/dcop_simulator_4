from plot_functions import *
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *
from impl_run_alg_once import run_alg_once


def run_alg_half_greedy(iteration, pos_list, targets_list, agents_list, objects_dict):
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


if __name__ == '__main__':
    LIFESPAN = 100
    SIDE_SIZE = 30
    run_alg_once(alg_func=run_alg_half_greedy, alg_name='greedy 2', side_size=SIDE_SIZE, lifespan=LIFESPAN)
