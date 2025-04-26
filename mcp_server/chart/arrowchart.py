import matplotlib.pyplot as plt
from typing import List, Union

class ArrowChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "",
                 color: str = "blue", width: float = 0.01, head_width: float = 0.05,
                 head_length: float = 0.1, length_includes_head: bool = True):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.width = width
        self.head_width = head_width
        self.head_length = head_length
        self.length_includes_head = length_includes_head

    def create_chart(self, x: float, y: float, dx: float, dy: float):
        fig, ax = plt.subplots()
        ax.arrow(x, y, dx, dy,
                 color=self.color,
                 width=self.width,
                 head_width=self.head_width,
                 head_length=self.head_length,
                 length_includes_head=self.length_includes_head)

        ax.set_xlim(min(x, x+dx) - 1, max(x, x+dx) + 1)
        ax.set_ylim(min(y, y+dy) - 1, max(y, y+dy) + 1)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig
