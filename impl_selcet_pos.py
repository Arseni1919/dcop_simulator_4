from GLOBALS import *
from dcop_dynamic import create_dynamic_dcop_setting


def distance(pos1, pos2):
    return math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2))


def select_pos(robot, targets, graph, robot_pos_name_set=None):
    if robot_pos_name_set is None:
        robot_pos_name_set = [pos_name for pos_name in robot.pos.neighbours]
        robot_pos_name_set.append(robot.pos.name)
    pos_dict_name_pos = {pos_node.name: pos_node.xy_pos for pos_node in graph}
    pos_dict_name_pos_node = {pos_node.name: pos_node for pos_node in graph}
    next_pos_name = select_pos_internal(robot, robot_pos_name_set, targets, pos_dict_name_pos)
    return pos_dict_name_pos_node[next_pos_name]


def select_pos_internal(robot, robot_pos_name_set, funcs, pos_dict_name_pos):
    max_func_value = max([target.req for target in funcs]) if len(funcs) > 0 else 0
    if len(robot_pos_name_set) == 1 or max_func_value < 1:
        return random.sample(robot_pos_name_set, 1)[0]
    target_set = []
    for target in funcs:
        if target.req == max_func_value:
            if any([distance(target.pos.xy_pos, pos_dict_name_pos[p_n]) < robot.sr for p_n in robot_pos_name_set]):
                target_set.append(target)

    if len(target_set) == 0:
        return random.sample(robot_pos_name_set, 1)[0]

    within_sr_range_list, target_set = within_sr_from_most(robot, robot_pos_name_set, target_set, pos_dict_name_pos)
    for target in target_set:
        funcs.remove(target)

    return select_pos_internal(robot, within_sr_range_list, funcs, pos_dict_name_pos)


def within_sr_from_most(robot, robot_pos_name_set, target_set, pos_dict_name_pos):
    within_sr_range_dict = {}
    max_list = []
    for robot_name in robot_pos_name_set:
        count = sum([distance(target.pos.xy_pos, pos_dict_name_pos[robot_name]) < robot.sr for target in target_set])
        max_list.append(count)
        within_sr_range_dict[robot_name] = count
    max_value = max(max_list)

    within_sr_range_list, target_set_to_send = [], []
    for robot_name, count in within_sr_range_dict.items():
        if count == max_value:
            within_sr_range_list.append(robot_name)
            target_set_to_send.extend(list(filter(
                lambda x: distance(x.pos.xy_pos, pos_dict_name_pos[robot_name]) < robot.sr,
                target_set
            )))
    target_set_to_send = list(set(target_set_to_send))
    return within_sr_range_list, target_set_to_send


def main():
    pos_list, targets_list, agents_list, objects_dict = create_dynamic_dcop_setting()
    chosen_pos = select_pos(robot=agents_list[0], targets=targets_list, graph=pos_list)
    print(f'chosen_pos: {chosen_pos.xy_pos}')


if __name__ == '__main__':
    main()
