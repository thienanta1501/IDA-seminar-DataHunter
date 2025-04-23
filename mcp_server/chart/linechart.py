import matplotlib.pyplot as plt

class LineChart:
    def __init__(self, title="", x_label="", y_label="",
                 linestyle='-', linewidth=2, marker=None, color=None,
                 scalex=True, scaley=True, label=None):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.marker = marker
        self.color = color
        self.scalex = scalex
        self.scaley = scaley
        self.label = label

    def create_chart(self, x, y):
        fig, ax = plt.subplots()

        ax.plot(
            x, y,
            linestyle=self.linestyle,
            linewidth=self.linewidth,
            marker=self.marker,
            color=self.color,
            scalex=self.scalex,
            scaley=self.scaley,
            label=self.label
        )

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        if self.label:
            ax.legend()

        return fig
