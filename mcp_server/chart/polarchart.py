import matplotlib.pyplot as plt
from typing import List, Union

class PolarChart:
    def __init__(self, title: str = "", color: str = "blue", linewidth: float = 1.5):
        self.title = title
        self.color = color
        self.linewidth = linewidth

    def create_chart(self, theta_data: List[Union[int, float]], r_data: List[Union[int, float]]):
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(theta_data, r_data, color=self.color, linewidth=self.linewidth)

        ax.set_title(self.title)
        
        return fig