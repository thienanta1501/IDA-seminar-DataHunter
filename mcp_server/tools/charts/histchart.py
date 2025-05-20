import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew

class HistChart:
    def __init__(self, title="", x_label="", y_label="", color="green", bins=10,
                 alpha=0.75, category=None, density=True, histtype="bar", stacked=False):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.bins = bins
        self.alpha = alpha
        self.category = category  
        self.density = density
        self.histtype = histtype
        self.stacked = stacked

    def create_chart(self, data):
        fig, ax = plt.subplots()
        title = self.title

        # Nếu có nhiều nhóm dữ liệu (theo category)
        if self.category:
            group_data = []
            group_labels = []
            group_colors = []

            default_colors = list(plt.get_cmap("tab10").colors)
            color_map = self.color if isinstance(self.color, list) else [self.color] * len(self.category)

            for idx, (label, values) in enumerate(self.category.items()):
                group_data.append(values)
                group_labels.append(label)
                # Dùng màu truyền vào, hoặc default nếu không đủ
                group_colors.append(color_map[idx] if idx < len(color_map) else default_colors[idx % len(default_colors)])

            ax.hist(group_data,
                    bins=self.bins,
                    #color=group_colors,
                    label=group_labels,
                    alpha=self.alpha,
                    density=self.density,
                    histtype=self.histtype,
                    stacked=self.stacked,
                    edgecolor='black')
        else:
            # Dữ liệu đơn
            ax.hist(data,
                    bins=self.bins,
                    color=self.color,
                    alpha=self.alpha,
                    density=self.density,
                    histtype=self.histtype,
                    edgecolor='black', label="histogram")
            sns.kdeplot(data, ax=ax, color=self.color, label="kde")
            skewness_value = skew(data)
            title = title + f"\n Skewness: {skewness_value}"
            ax.legend()

        ax.set_title(title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        fig.tight_layout()

        return fig