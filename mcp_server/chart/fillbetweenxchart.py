import matplotlib.pyplot as plt
from typing import List, Union

class FillBetweenXChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "",
                 color: str = "blue", alpha: float = 0.5, step: str = None,
                 interpolate: bool = False):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.alpha = alpha
        self.step = step
        self.interpolate = interpolate

    def create_chart(self, y: List[Union[int, float]], x1: List[Union[int, float]], x2: Union[List[Union[int, float]], float] = 0,
                     where: Union[List[bool], None] = None):
        fig, ax = plt.subplots()
        ax.fill_betweenx(y, x1, x2=x2, where=where, step=self.step,
                         interpolate=self.interpolate, color=self.color, alpha=self.alpha)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig