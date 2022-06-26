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
    file_name = 'data/2022-6-26-17-40_problems_1__iters_10_cov.json'
    big_cov_dict, algs_to_compare, lifespan = open_data(file_name)
    plot_big_cov_graph(big_cov_dict, algs_to_compare, lifespan)

    file_name = 'data/2022-6-26-17-40_problems_1__iters_10_col.json'
    big_col_dict, algs_to_compare, lifespan = open_data(file_name)
    plot_big_col_graph(big_col_dict, algs_to_compare, lifespan)


if __name__ == '__main__':
    main()