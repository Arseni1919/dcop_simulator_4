from functions import *

#
# def calc_target_remained_cov(agents_list, target, up_value):
#     sum_of_creds = 0
#     for agent in agents_list:
#         dist = distance_nodes(target.pos, agent.pos)
#         if dist < agent.sr:
#             sum_of_creds += agent.cred
#     target_remained_cov = max(0, up_value * target.req - sum_of_creds)
#     return target_remained_cov
#
#
# def get_coverage_value(targets_list, agents_list, i_time):
#     total_remained_cov = 0
#     for target in targets_list:
#         up_value = target.up_values[i_time]
#         if up_value > 0:
#             target_remained_cov = calc_target_remained_cov(agents_list, target, up_value)
#             total_remained_cov += target_remained_cov
#
#     return total_remained_cov