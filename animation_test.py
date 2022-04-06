import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

fig = plt.figure()
nx = ny = 20
data = np.random.rand(nx, ny)
ax = sns.heatmap(data, vmin=0, vmax=1)

def init():
    plt.clf()
    ax = sns.heatmap(data, vmin=0, vmax=1)

def animate(i):
    plt.clf()
    data = np.random.rand(nx, ny)
    ax = sns.heatmap(data, vmin=0, vmax=1)

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=200)

plt.show()

