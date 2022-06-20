import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)


fig = plt.figure()
fig.add_subplot(1, 2, 1)   #top and bottom left
fig.add_subplot(2, 2, 2)   #top right
fig.add_subplot(2, 2, 4)   #bottom right
plt.show()