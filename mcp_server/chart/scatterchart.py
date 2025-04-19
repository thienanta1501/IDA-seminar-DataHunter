import matplotlib.pyplot as plt

class ScatterChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "", color: str = "skyble"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color

    def create_chart(self, x_data: list, y_data: list):
        fig, ax = plt.subplots()
        ax.scatter(x_data, y_data, color=self.color)
        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig