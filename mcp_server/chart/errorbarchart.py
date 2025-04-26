import matplotlib.pyplot as plt
from typing import List, Union, Optional

class ErrorBarChart:
    def __init__(self, title: str = "", x_label: str = "", y_label: str = "",
                 fmt: str = "o", color: Optional[str] = None, ecolor: Optional[str] = None,
                 elinewidth: Optional[float] = None, capsize: Optional[float] = None,
                 barsabove: bool = False, errorevery: int = 1, capthick: Optional[float] = None):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.fmt = fmt
        self.color = color
        self.ecolor = ecolor
        self.elinewidth = elinewidth
        self.capsize = capsize
        self.barsabove = barsabove
        self.errorevery = errorevery
        self.capthick = capthick

    def create_chart(self,
                     x_data: List[Union[int, float]],
                     y_data: List[Union[int, float]],
                     yerr: Optional[Union[float, List[float]]] = None,
                     xerr: Optional[Union[float, List[float]]] = None):
        fig, ax = plt.subplots()
        ax.errorbar(x_data, y_data, yerr=yerr, xerr=xerr,
                    fmt=self.fmt, color=self.color, ecolor=self.ecolor,
                    elinewidth=self.elinewidth, capsize=self.capsize,
                    barsabove=self.barsabove, errorevery=self.errorevery,
                    capthick=self.capthick)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        return fig
