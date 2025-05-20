import matplotlib.pyplot as plt
from itertools import cycle

class LineChart:
    def __init__(self, title="", x_label="", y_label="",
                 linestyle='-', linewidth=2, marker=None, color=None,
                 scalex=True, scaley=True):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.marker = marker
        self.color = color
        self.scalex = scalex
        self.scaley = scaley

    def create_chart(self, x_data: list, y_data: dict):
        fig, ax = plt.subplots()
        labels = list(y_data.keys())
        print(labels)

        colors = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k']) 

        for label in labels:
            ax.plot(x_data, y_data[label], label = label, color=next(colors))

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        ax.xaxis.set_tick_params(rotation=90)

        if len(labels) > 1:
            ax.legend()

        fig.tight_layout()

        return fig