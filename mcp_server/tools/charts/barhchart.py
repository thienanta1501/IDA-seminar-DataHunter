import matplotlib.pyplot as plt
import numpy as np
class BarhChart:
    def __init__(self, title="", x_label="", y_label="", color="blue",
                 width=0.8, left=None, align='center', type="simple"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.width = width
        self.left = left  # analogous to 'bottom' in vertical bar charts
        self.align = align
        self.type = type

    def create_chart(self, y_data_labels, x_data_dict):
        fig, ax = plt.subplots()
        keys = list(x_data_dict.keys())

        if not keys:
            raise ValueError("x_data_dict must contain at least one data series.")

        # Grouped horizontal bar chart
        if self.type == "grouped" or (len(list(x_data_dict.keys())) > 1 and self.type == "simple"):
            num_series = len(keys)
            y = np.arange(len(y_data_labels))
            bar_height = self.width / num_series

            for i, key in enumerate(keys):
                offset = (i - num_series / 2) * bar_height + bar_height / 2
                ax.barh(
                    y + offset,
                    width=x_data_dict[key],
                    height=bar_height,
                    label=key
                )

            ax.set_yticks(y)
            ax.set_yticklabels(y_data_labels)

        # Simple horizontal bar
        elif self.type == "simple":
            ax.barh(
                y=y_data_labels,
                width=x_data_dict[keys[0]],
                color=self.color,
                height=self.width,
                left=self.left,
                align=self.align
            )

        # Stacked horizontal bar chart
        elif self.type == "stacked":
            y = np.arange(len(y_data_labels))
            left = np.zeros(len(y_data_labels))

            for key in keys:
                values = np.array(x_data_dict[key])
                ax.barh(
                    y,
                    width=values,
                    left=left,
                    label=key
                )
                left += values

            ax.set_yticks(y)
            ax.set_yticklabels(y_data_labels)

        # Common chart settings
        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.legend()

        fig.tight_layout()

        return fig