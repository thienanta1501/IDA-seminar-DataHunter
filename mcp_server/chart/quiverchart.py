import matplotlib.pyplot as plt
from typing import List, Union

class QuiverChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "", color: str = "blue", scale: float = 1.0):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.scale = scale

    def create_chart(self, x_data: List[Union[int, float]], y_data: List[Union[int, float]],
                     u_data: List[Union[int, float]], v_data: List[Union[int, float]]):
        fig, ax = plt.subplots()
        ax.quiver(x_data, y_data, u_data, v_data, color=self.color, scale=self.scale)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig
