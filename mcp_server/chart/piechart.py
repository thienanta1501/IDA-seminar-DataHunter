# chart/piechart.py
import matplotlib.pyplot as plt

class PieChart:
    def __init__(self, title="", colors=None):
        self.title = title
        self.colors = colors  # Optional list of colors

    def create_chart(self, labels, values):
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=self.colors, startangle=90)
        ax.set_title(self.title)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
        return fig