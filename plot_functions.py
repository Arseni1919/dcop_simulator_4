import matplotlib.pyplot as plt

from GLOBALS import *


class PlotField:
    def __init__(self, side_size):
        self.side_size = side_size
        self.fig, (self.ax, self.ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        self.fig.tight_layout()

    def plot_field(self, i, pos_list, targets_list, agents_list, objects_dict):
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
        x_target_list = [node.pos.x for node in targets_list]
        y_target_list = [node.pos.y for node in targets_list]
        self.ax.scatter(x_target_list, y_target_list, marker='s', color='orange', s=40, alpha=0.7)
        # for target_node in targets_list:
        #     matplotlib.patches.Circle(xy, radius=5, **kwargs)

        # agent nodes
        x_agent_list = [node.pos.x for node in agents_list]
        y_agent_list = [node.pos.y for node in agents_list]
        self.ax.scatter(x_agent_list, y_agent_list, marker='o', color='blue', s=40, alpha=0.7)

        # plt.show()
        plt.pause(0.05)


# def plot_field(pos_list, targets_list, agents_list, objects_dict):
#     f = plt.figure()
#     side = 7
#     f.set_figwidth(side)
#     f.set_figheight(side)
#     f.tight_layout()
#
#     # pos nodes
#     x_pos_list = [node.x for node in pos_list]
#     y_pos_list = [node.y for node in pos_list]
#     plt.scatter(x_pos_list, y_pos_list, marker='s', color='gray', s=3, alpha=0.3)
#
#     # target nodes
#     x_target_list = [node.pos.x for node in targets_list]
#     y_target_list = [node.pos.y for node in targets_list]
#     plt.scatter(x_target_list, y_target_list, marker='s', color='orange', s=40, alpha=0.87)
#     # for target_node in targets_list:
#     #     matplotlib.patches.Circle(xy, radius=5, **kwargs)
#
#     # agent nodes
#     pass
#
#     plt.title('Field')
#     plt.show()


def main():
    pass


if __name__ == '__main__':
    main()
