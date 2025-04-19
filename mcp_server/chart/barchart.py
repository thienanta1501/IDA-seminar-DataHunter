import matplotlib.pyplot as plt

class BarChart:
    def __init__(self, title ="", x_label = "", y_label = "", color = "blue"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color

    def create_chart(self, x_data, y_data):
        fig, ax = plt.subplots()
        ax.bar(x_data, y_data, color=self.color)
        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig