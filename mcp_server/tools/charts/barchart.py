import matplotlib.pyplot as plt
import numpy as np

class BarChart:
    def __init__(self, title ="", x_label = "", y_label = "", color = "blue", 
                 width = 0.8, bottom = None, align='center', type = "simple"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.width = width
        self.bottom = bottom
        self.align = align
        self.type = type

    def create_chart(self, x_data, y_data):
        fig, ax = plt.subplots()
        keys_of_dict = list(y_data.keys())

        if self.type == "grouped" or (len(list(y_data.keys())) > 1 and self.type=="simple"):
            num_columns = len(keys_of_dict)
            x = np.arange(len(x_data))
            width = self.width / num_columns

            for i, key in enumerate(keys_of_dict):
                offset = (i - num_columns / 2) * width + width / 2
                ax.bar(x + offset, 
                    height=y_data[key], 
                    width=width,
                    label=key)
            ax.set_xticks(x)   
            ax.set_xticklabels(x_data)
        elif self.type == "simple":
            ax.bar(x=x_data, 
                height=y_data[keys_of_dict[0]], 
                color=self.color,
                width=self.width,
                bottom=self.bottom,
                align=self.align)
        elif self.type == "stacked":
            x = np.arange(len(x_data))
            bottom = np.zeros(len(x_data))

            for category in keys_of_dict:
                values = np.array(y_data[category])
                ax.bar(x, values, bottom=bottom, label=category)
                bottom += values

            ax.set_xticks(x)
            ax.set_xticklabels(x_data)

        

        
        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.legend()

        fig.tight_layout()

        return fig