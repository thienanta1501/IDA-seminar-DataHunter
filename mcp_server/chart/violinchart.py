import matplotlib.pyplot as plt

class ViolinPlotChart:
    def __init__(self, title="", x_label="", y_label="",
                 orientation="vertical", widths=0.5, showmeans=False,
                 showextrema=True, showmedians=False, quantiles=None,
                 points=100, bw_method=None, side='both', category=None):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.orientation = orientation
        self.widths = widths
        self.showmeans = showmeans
        self.showextrema = showextrema
        self.showmedians = showmedians
        self.quantiles = quantiles
        self.points = points
        self.bw_method = bw_method
        self.side = side
        self.category = category  # dict[str, list] nếu nhiều nhóm

    def create_chart(self):
        fig, ax = plt.subplots()

        if not self.category or not isinstance(self.category, dict):
            raise ValueError("Category must be a dictionary with group labels and values.")

        data = list(self.category.values())
        positions = list(range(1, len(data) + 1))

        parts = ax.violinplot(dataset=data,
                              positions=positions,
                              vert=(self.orientation == "vertical"),
                              widths=self.widths,
                              showmeans=self.showmeans,
                              showextrema=self.showextrema,
                              showmedians=self.showmedians,
                              quantiles=self.quantiles,
                              points=self.points,
                              bw_method=self.bw_method,
                              side=self.side)

        # Thêm nhãn nhóm trên trục x
        if self.orientation == "vertical":
            ax.set_xticks(positions)
            ax.set_xticklabels(list(self.category.keys()))
        else:
            ax.set_yticks(positions)
            ax.set_yticklabels(list(self.category.keys()))

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig
