import matplotlib.pyplot as plt

class ScatterChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = ""):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def create_chart(self, x_data: list, y_data: list, colors: list = None, sizes: list = None):
        fig, ax = plt.subplots()

        if colors is not None and sizes is not None:
            ax.scatter(x_data, y_data, c=colors, s=sizes, alpha=0.5)
        elif colors is not None:
            ax.scatter(x_data, y_data, c=colors, alpha=0.5)
        elif sizes is not None:
            ax.scatter(x_data, y_data, s=sizes, alpha=0.5)
        else:
            ax.scatter(x_data, y_data, color=self.color)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig