from impl_alg_random import run_alg_random
from impl_alg_greedy import run_alg_greedy
from impl_alg_dsa_mst import run_alg_dsa_mst
from impl_alg_greedy_select_pos import run_alg_greedy_select_pos
from impl_alg_cadsa import run_alg_cadsa
from impl_alg_ca_greedy_select_pos import run_alg_ca_greedy_select_pos
from impl_alg_dssa import run_alg_dssa
from impl_alg_ms_mst import run_alg_max_sum_mst
from impl_alg_cams import run_alg_cams
from impl_alg_ms_mst_breakdowns import run_max_sum_mst_breakdowns
from impl_alg_hard_constrained_ms_mst import run_alg_hard_constrained_ms_mst
from impl_alg_hard_constrained_cams import run_alg_hard_constrained_cams

algs_dict = {
        'random': run_alg_random,
        'greedy': run_alg_greedy,
        'dsa_mst': run_alg_dsa_mst,
        'greedy_select_pos': run_alg_greedy_select_pos,
        'ca_select_pos': run_alg_ca_greedy_select_pos,
        'cadsa': run_alg_cadsa,
        'dssa': run_alg_dssa,
        'max_sum_mst': run_alg_max_sum_mst,
        'max_sum_mst - breakdowns': run_max_sum_mst_breakdowns,
        'cams': run_alg_cams,
        'hard_constrained_ms': run_alg_hard_constrained_ms_mst,
        'hard_constrained_cams': run_alg_hard_constrained_cams,

    }

labels_dict = {
        'random': 'Random',
        'greedy': 'Greedy',
        'dsa_mst': 'DSA_MST',
        'greedy_select_pos': 'Greedy select_pos',
        'ca_select_pos': 'CA select_pos',
        'cadsa': 'CADSA',
        'dssa': 'DSSA',
        'max_sum_mst': 'Max-sum_MST',
        'max_sum_mst - breakdowns': 'Max-sum_MST with breakdowns',
        'cams': 'CAMS',
        'hard_constrained_ms': 'hard_constrained_ms',
        'hard_constrained_cams': 'hard_constrained_cams',
}
