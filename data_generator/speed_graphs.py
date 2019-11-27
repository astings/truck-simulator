"""Script generating different graphs for speed visualisation."""

from truck import Truck
from matplotlib import pyplot as plt


def dual_axis_plot(x_data, y1_data, y2_data, **kwargs):
    fig, ax1 = plt.subplots()
    label_x = kwargs.get('x_label', '')
    label_y1 = kwargs.get('y1_label', '')
    label_y2 = kwargs.get('y2_label', '')
    color_y1 = kwargs.get('y1_color', 'tab:red')
    color_y2 = kwargs.get('y2_color', 'tab:blue')
    path = kwargs.get('path', 'graph.png')

    ax1.plot(x_data, y1_data, color=color_y1)
    ax1.set_xlabel(label_x)
    ax1.set_ylabel(label_y1)
    ax2 = ax1.twinx()
    ax2.plot(x_data, y2_data, color=color_y2)
    ax2.set_ylabel(label_y2)

    fig.tight_layout()
    plt.savefig(path)


t = Truck(id=1)
t.drive()
coord = t.get_coordinates()
distances = [i*10 for i in range(len(coord))]
timestamps = [elt[2] for elt in coord]
speed = [elt[3] * 3.6 for elt in coord]
dual_axis_plot(x_data=distances,
               y1_data=timestamps,
               y2_data=speed,
               x_label="Distance",
               y1_label='Timestamps (s)',
               y2_label='speed (km/h)')