import matplotlib.pyplot as plt
from typing import List, Union, Optional

class FillBetweenChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "", color: str = "blue",
                 alpha: float = 0.5, step: Optional[str] = None, interpolate: bool = False):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.alpha = alpha
        self.step = step
        self.interpolate = interpolate

    def create_chart(self,
                     x_data: List[Union[str, int, float]],
                     y1_data: List[Union[int, float]],
                     y2_data: Union[List[Union[int, float]], int, float] = 0,
                     where: Optional[List[bool]] = None):
        fig, ax = plt.subplots()
        ax.fill_between(x_data, y1_data, y2=y2_data, where=where,
                        interpolate=self.interpolate, step=self.step,
                        color=self.color, alpha=self.alpha)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        return fig
