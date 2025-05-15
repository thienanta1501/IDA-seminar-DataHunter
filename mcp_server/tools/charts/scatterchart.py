import matplotlib.pyplot as plt

class ScatterChart:
    def __init__(self, x, y, s=None, c=None, marker=None, cmap=None, vmin=None, vmax=None,
                 alpha=None, linewidths=None, edgecolors=None, plotnonfinite=False, title=None, **kwargs):
        self.x = x
        self.y = y
        self.s = s
        self.c = c  # You can pass this directly in case of color or use colorizer
        self.marker = marker
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax
        self.alpha = alpha
        self.linewidths = linewidths
        self.edgecolors = edgecolors
        self.plotnonfinite = plotnonfinite
        self.title = title  # Title for the plot
        self.kwargs = kwargs

    def create_chart(self):
        fig, ax = plt.subplots()

        # # Handle the color argument (use colorizer logic if needed, otherwise use direct c)
        # if self.colorizer:
        #     c = self.colorizer(self.x, self.y)  # Example of colorizer function application
        # else:
        #     c = self.c  # Use the provided color

        # Create scatter plot
        scatter = ax.scatter(self.x, self.y, s=self.s, c=self.c, marker=self.marker, cmap=self.cmap, vmin=self.vmin, vmax=self.vmax, alpha=self.alpha,
                            linewidths=self.linewidths, edgecolors=self.edgecolors, 
                            plotnonfinite=self.plotnonfinite, **self.kwargs)
        
        # Set the title if provided
        if self.title:
            ax.set_title(self.title)

        fig.tight_layout()

        return fig