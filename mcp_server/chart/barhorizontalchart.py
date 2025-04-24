import matplotlib.pyplot as plt

class BarhChart:
    def __init__(self, title="", x_label="", y_label="", color="green", height=0.8,
                 align="center", category=None, left=None):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.height = height
        self.align = align
        self.category = category  # Dict[str, numeric]
        self.left = left

    def create_chart(self, data):
        fig, ax = plt.subplots()

        if self.category:
            y_labels = list(self.category.keys())
            values = list(self.category.values())

            color_map = self.color if isinstance(self.color, list) else [self.color] * len(values)
            for i, (y, val) in enumerate(zip(y_labels, values)):
                ax.barh(y=y, width=val,
                        height=self.height,
                        left=self.left,
                        align=self.align,
                        color=color_map[i] if i < len(color_map) else 'gray',
                        edgecolor='black')

        else:
            # Trường hợp không có category, dữ liệu đơn
            y_pos = list(range(len(data)))
            ax.barh(y=y_pos, width=data,
                    height=self.height,
                    left=self.left,
                    align=self.align,
                    color=self.color,
                    edgecolor='black')
            ax.set_yticks(y_pos)

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        return fig
