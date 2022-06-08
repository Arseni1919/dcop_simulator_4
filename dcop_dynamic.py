from GLOBALS import *
from nodes import TargetNode, AgentNode, PosNode
from plot_functions import *


def create_dynamic_dcop_setting(lifespan=100, n_agents=30, agent_sr=10, n_targets=10, target_decay_rate=3,
                                target_min_life=10, target_max_life=30, side_size=50):
    pos_list = []
    targets_list = []
    agents_list = []
    objects_dict = {}

    # create positions
    for x in range(1, side_size + 1):
        for y in range(1, side_size + 1):
            new_pos = PosNode(x, y)
            pos_list.append(new_pos)
            objects_dict[new_pos.name] = new_pos

    # create targets
    nodes_for_targets = random.sample(pos_list, n_targets)
    for i in range(n_targets):
        new_target = TargetNode(i, decay_rate=target_decay_rate, min_life=target_min_life, max_life=target_max_life,
                                lifespan=lifespan, pos=nodes_for_targets[i])
        targets_list.append(new_target)
        objects_dict[new_target.name] = new_target

    # create agents
    nodes_for_agents = random.sample(pos_list, n_agents)
    for i in range(n_agents):
        new_agent = AgentNode(i, sr=agent_sr, pos=nodes_for_agents[i])
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
        plotter.plot_field(i, pos_list, targets_list, agents_list, objects_dict)


if __name__ == '__main__':
    LIFESPAN = 100
    N_TARGETS = 10
    N_AGENTS = 30
    DECAY_RATE = 3
    MIN_LIFE = 10
    MAX_LIFE = 30
    SIDE_SIZE = 50
    SR = 10

    main()
