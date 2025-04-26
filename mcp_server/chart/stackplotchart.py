import matplotlib.pyplot as plt

class StackPlotChart:
    def __init__(self, title="", x_label="", y_label="", colors=None, baseline="zero",
                 hatch=None, category=None):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.colors = colors
        self.baseline = baseline
        self.hatch = hatch
        self.category = category  # dict[str, list of y-values]

    def create_chart(self, x):
        fig, ax = plt.subplots()

        if self.category is None or len(self.category) == 0:
            raise ValueError("Category data must be provided for stackplot.")

        labels = list(self.category.keys())
        y_values = list(self.category.values())

        if any(len(y) != len(x) for y in y_values):
            raise ValueError("All y-series in category must match the length of x.")

        color_map = self.colors if self.colors else plt.get_cmap("tab10").colors[:len(labels)]

        stack = ax.stackplot(x, *y_values,
                             labels=labels,
                             colors=color_map,
                             baseline=self.baseline,
                             hatch=self.hatch)

        ax.legend(loc="upper left")
        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig
