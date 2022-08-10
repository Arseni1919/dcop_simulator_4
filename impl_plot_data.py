from functions import *
from plot_functions import *


def get_algs_to_compare(big_dict):
    algs_to_compare = list(big_dict.keys())
    return algs_to_compare


def get_lifespan(big_dict):
    some_value = list(big_dict.values())[0]
    return len(some_value)


def open_data(file_name):
    f = open(file_name)
    big_dict = json.load(f)
    algs_to_compare = get_algs_to_compare(big_dict)
    lifespan = get_lifespan(big_dict)
    f.close()
    return big_dict, algs_to_compare, lifespan


def main():
    # Opening JSON file
    # folder_name = f'2022-7-10-22-4_problems_50__iters_120_dynamic'
    # folder_name = f'2022-8-5-21-37_problems_20__iters_40_'
    folder_name = f'2022-7-10-22-57_problems_50__iters_120_static'

    # folder_name = f'2022-8-7-20-40_problems_20__iters_40_dynamic_RAND_POS_NEI'
    # folder_name = f'2022-8-7-22-42_problems_20__iters_40_static_RAND_POS_NEI'

    # adding = '2022-7-1-17-56_problems_20__iters_50'
    # file_name = f'data/{adding}_cov.json'

    algs_to_plot = ['cams', 'max_sum_mst - breakdowns', 'max_sum_mst', 'dssa', 'cadsa', 'dsa_mst', 'random']
    # algs_to_plot = None

    file_name = f'data/{folder_name}/cov.json'
    big_cov_dict, algs_to_compare, lifespan = open_data(file_name)
    plot_big_cov_graph(big_cov_dict, algs_to_compare, lifespan, algs_to_plot=algs_to_plot)

    # file_name = f'data/{adding}_col.json'

    file_name = f'data/{folder_name}/col.json'
    big_col_dict, algs_to_compare, lifespan = open_data(file_name)
    plot_big_col_graph(big_col_dict, algs_to_compare, lifespan, algs_to_plot=algs_to_plot)


if __name__ == '__main__':
    main()
