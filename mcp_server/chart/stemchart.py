import matplotlib.pyplot as plt
from typing import List, Union

class StemChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "",
                 linefmt: str = "C0-", markerfmt: str = "C0o", basefmt: str = "k-",
                 bottom: float = 0, orientation: str = "vertical"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.linefmt = linefmt
        self.markerfmt = markerfmt
        self.basefmt = basefmt
        self.bottom = bottom
        self.orientation = orientation

    def create_chart(self, x_data: List[Union[int, float, str]], y_data: List[Union[int, float]]):
        fig, ax = plt.subplots()
        ax.stem(x_data, y_data,
                linefmt=self.linefmt,
                markerfmt=self.markerfmt,
                basefmt=self.basefmt,
                bottom=self.bottom,
                orientation=self.orientation)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig
