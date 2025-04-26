import matplotlib.pyplot as plt
from typing import List, Union

class StepChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "", color: str = "blue",
                 linestyle: str = "-", marker: str = "", linewidth: float = 1.5, where: str = "pre"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.linestyle = linestyle
        self.marker = marker
        self.linewidth = linewidth
        self.where = where

    def create_chart(self, x_data: List[Union[int, float]], y_data: List[Union[int, float]]):
        fig, ax = plt.subplots()
        ax.step(x_data, y_data, where=self.where, color=self.color, linestyle=self.linestyle,
                marker=self.marker, linewidth=self.linewidth)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig