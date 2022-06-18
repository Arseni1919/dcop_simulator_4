from GLOBALS import *
from nodes import TargetNode, AgentNode, PosNode
from plot_functions import *
from functions import *


def connect_neighbours(pos_list):
    for pos_1 in pos_list:
        for pos_2 in pos_list:
            if pos_1.name != pos_2.name and pos_1.name not in pos_2.neighbours:
                distance = distance_nodes(pos_1, pos_2)
                if distance < 1.01:
                    pos_1.neighbours.append(pos_2.name)
                    pos_2.neighbours.append(pos_1.name)


def create_dynamic_dcop_setting(lifespan=120, n_agents=30, agent_sr=5, n_targets=30, target_decay_rate=3,
                                target_min_life=40, target_max_life=50, side_size=30):
    pos_list = []
    targets_list = []
    agents_list = []
    objects_dict = {}

    # create positions
    print('creating positions...')
    for x in range(1, side_size + 1):
        for y in range(1, side_size + 1):
            new_pos = PosNode(x, y)
            pos_list.append(new_pos)
            objects_dict[new_pos.name] = new_pos

    connect_neighbours(pos_list)

    # create targets
    print('creating targets...')
    nodes_for_targets = random.sample(pos_list, n_targets)
    for i in range(n_targets):
        new_target = TargetNode(i, decay_rate=target_decay_rate, min_life=target_min_life, max_life=target_max_life,
                                lifespan=lifespan, pos=nodes_for_targets[i])
        targets_list.append(new_target)
        objects_dict[new_target.name] = new_target

    # create agents
    print('creating agents...')
    nodes_for_agents = random.sample(pos_list, n_agents)
    for i in range(n_agents):
        new_agent = AgentNode(i, sr=agent_sr, pos=nodes_for_agents[i], cred=random.randint(25, 51))
        agents_list.append(new_agent)
        objects_dict[new_agent.name] = new_agent

    return pos_list, targets_list, agents_list, objects_dict


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
        for agent in agents_list:
            rand_choice = objects_dict[random.choice(agent.pos.neighbours)]
            agent.pos = rand_choice
        coverage_value = get_coverage_value(targets_list, agents_list, i_time=i)
        plotter.update_tracker('rand', coverage_value)
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
