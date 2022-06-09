import matplotlib.pyplot as plt

from GLOBALS import *


class PlotField:
    def __init__(self, side_size):
        self.side_size = side_size
        self.fig, (self.ax, self.ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        self.fig.tight_layout()
        self.tracker = {}

    @staticmethod
    def show():
        plt.show()

    def close(self):
        self.ax.clear()
        self.ax2.clear()
        self.tracker = {}
        plt.close()

    def update_tracker(self, alg_name, coverage_value):
        if alg_name not in self.tracker:
            self.tracker[alg_name] = []
        self.tracker[alg_name].append(coverage_value)

    def plot_field(self, i, pos_list, targets_list, agents_list, lifespan=100):
        self.ax.clear()
        padding = 2
        self.ax.set_xlim([0 - padding, self.side_size + padding])
        self.ax.set_ylim([0 - padding, self.side_size + padding])

        # TITLES
        # self.ax.set_title(alg_name)
        self.ax.set_title('Field')

        # pos nodes
        x_pos_list = [node.x for node in pos_list]
        y_pos_list = [node.y for node in pos_list]
        self.ax.scatter(x_pos_list, y_pos_list, marker='s', color='gray', s=3, alpha=0.3)

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

        self.ax2.clear()
        self.ax2.set_xlim(0, lifespan)
        for i_alg, i_data in self.tracker.items():
            self.ax2.plot(list(range(len(i_data))), i_data, label=i_alg)
        self.ax2.legend()
        plt.pause(0.05)


def main():
    pass


if __name__ == '__main__':
    main()
