from GLOBALS import *
from plot_functions import PlotField
from dcop_dynamic import create_dynamic_dcop_setting
from functions import *


def run_alg_once(alg_func, alg_name, side_size=30, lifespan=120, const_app=False):
    plotter = PlotField(side_size=side_size)
    pos_list, targets_list, agents_list, objects_dict = create_dynamic_dcop_setting(
        lifespan=lifespan,
        side_size=side_size,
        const_app=const_app
    )

    for i in range(lifespan):
        print(f'\riteration: {i}', end='')
        if i == 86:
            print()
            # vertex conf.: agent 28 [(37, 5) -> (38, 5)] - agent 86 [(39, 5) -> (38, 5)]

        alg_func(i, pos_list, targets_list, agents_list, objects_dict)
        coverage_value = get_coverage_value(targets_list, agents_list, i_time=i)
        collisions_value = get_collisions_value(targets_list, agents_list, i_time=i)
        plotter.update_trackers(f'{alg_name}', coverage_value, collisions_value)
        # plotter.plot_field(i, pos_list, targets_list, agents_list, lifespan=lifespan)

        if i >= 85:
            plotter.plot_field(i, pos_list, targets_list, agents_list, lifespan=lifespan)

    plotter.show()


def main():
    pass


if __name__ == '__main__':
    main()
