import matplotlib.pyplot as plt

from GLOBALS import *

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

class PlotField:
    def __init__(self, side_size, life_plot=True):
        self.side_size = side_size
        self.life_plot = life_plot
        if self.life_plot:
            self.fig = plt.figure(figsize=(12, 6))
            self.ax = self.fig.add_subplot(1, 2, 1)  # top and bottom left
            self.ax2 = self.fig.add_subplot(2, 2, 2)  # top right
            self.ax3 = self.fig.add_subplot(2, 2, 4)  # bottom right
            # self.fig, (self.ax, self.ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
            self.fig.tight_layout()

        self.coverage_tracker = {}
        self.collisions_tracker = {}

    def show(self):
        if self.life_plot:
            plt.show()

    def clean_trackers(self):
        self.coverage_tracker = {}
        self.collisions_tracker = {}

    def close(self):
        self.clean_trackers()
        if self.life_plot:
            self.ax.clear()
            self.ax2.clear()
            plt.close()

    def update_trackers(self, alg_name, coverage_value, collisions_value):

        if alg_name not in self.coverage_tracker:
            self.coverage_tracker[alg_name] = []
        self.coverage_tracker[alg_name].append(coverage_value)

        if alg_name not in self.collisions_tracker:
            self.collisions_tracker[alg_name] = []
        self.collisions_tracker[alg_name].append(collisions_value)

    def plot_field(self, i, pos_list, targets_list, agents_list, objects_dict=None, lifespan=100):
        if self.life_plot:
            # AX 1
            self.ax.clear()
            padding = 2
            self.ax.set_xlim([0 - padding, self.side_size + padding])
            self.ax.set_ylim([0 - padding, self.side_size + padding])

            # TITLE
            # self.ax.set_title(alg_name)
            self.ax.set_title('Field')

            # pos nodes
            x_pos_list = [node.x for node in pos_list]
            y_pos_list = [node.y for node in pos_list]
            self.ax.scatter(x_pos_list, y_pos_list, marker='s', color='gray', s=3, alpha=0.3)

            # pos neighbours
            if objects_dict:
                for main_pos in pos_list:
                    for nei_pos_name in main_pos.neighbours:
                        nei_pos = objects_dict[nei_pos_name]
                        x1, y1 = [main_pos.x, nei_pos.x], [main_pos.y, nei_pos.y]
                        self.ax.plot(x1, y1, color='k')

            # target nodes
            # x_target_list = [node.pos.x for node in targets_list]
            # y_target_list = [node.pos.y for node in targets_list]
            # self.ax.scatter(x_target_list, y_target_list, marker='s', color='orange', s=40, alpha=0.7)
            min_sr = min([agent.sr for agent in agents_list])
            for t_node in targets_list:
                self.ax.scatter(t_node.pos.x, t_node.pos.y, marker='s', color='orange', s=40, alpha=t_node.up_values[i])
                circle_sr = plt.Circle((t_node.pos.x, t_node.pos.y), min_sr, color='orange', alpha=0.2 * t_node.up_values[i])
                self.ax.add_patch(circle_sr)

            # agent nodes
            x_agent_list = [node.pos.x for node in agents_list]
            y_agent_list = [node.pos.y for node in agents_list]
            self.ax.scatter(x_agent_list, y_agent_list, marker='o', color='blue', s=40, alpha=0.7)

            # --------------------------------------------------------- #
            # AX 2
            self.ax2.clear()
            self.ax2.set_xlim(0, lifespan)
            for i_alg, i_data in self.coverage_tracker.items():
                self.ax2.plot(list(range(len(i_data))), i_data, label=i_alg)
            self.ax2.legend()
            self.ax2.set_ylabel('remained coverage')

            # --------------------------------------------------------- #
            # AX 3
            self.ax3.clear()
            self.ax3.set_xlim(0, lifespan)
            for i_alg, i_data in self.collisions_tracker.items():
                self.ax3.plot(list(range(len(i_data))), np.cumsum(i_data), label=i_alg)
            self.ax3.legend()
            self.ax3.set_ylabel('collisions')
            plt.pause(0.05)


def plot_big_cov_graph(big_cov_dict, algs_to_compare, lifespan):
    for alg_name in algs_to_compare:
        plt.plot(range(lifespan), np.mean(big_cov_dict[alg_name], axis=1), label=labels_dict[alg_name])
    plt.ylabel('Remained Coverage Requirement', fontsize=28)
    plot_design()


def plot_big_col_graph(big_col_dict, algs_to_compare, lifespan):
    for alg_name in algs_to_compare:
        plt.plot(range(lifespan), np.mean(np.cumsum(big_col_dict[alg_name], axis=0), axis=1), label=labels_dict[alg_name])
    plt.ylabel('Collisions', fontsize=28)
    plot_design()


def plot_design():
    plt.rcParams.update({'font.size': 18})
    plt.legend(frameon=False, loc='upper left')
    # plt.legend(frameon=True, loc='upper left')
    plt.tight_layout()
    plt.show()


def main():
    pass


if __name__ == '__main__':
    main()
