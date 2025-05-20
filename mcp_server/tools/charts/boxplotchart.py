import matplotlib.pyplot as plt

class BoxPlotChart:
    def __init__(self, title="", x_label="", y_label="", notch=False, vert=True,
                 patch_artist=True, boxprops=None, medianprops=None, flierprops=None,
                 whiskerprops=None, capprops=None, showmeans=False, meanprops=None,
                 widths=None, positions=None, showcaps=True, showbox=True,
                 showfliers=True):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.notch = notch
        self.vert = vert
        self.patch_artist = patch_artist
        self.boxprops = boxprops or {}
        self.medianprops = medianprops or {}
        self.flierprops = flierprops or {}
        self.whiskerprops = whiskerprops or {}
        self.capprops = capprops or {}
        self.showmeans = showmeans
        self.meanprops = meanprops or {}
        self.widths = widths
        self.positions = positions
        self.showcaps = showcaps
        self.showbox = showbox
        self.showfliers = showfliers

    def create_chart(self, data):
        fig, ax = plt.subplots()

        labels = list(data.keys())
        data_values = list(data.values())

        bp = ax.boxplot(
            data_values,
            notch=self.notch,
            vert=self.vert,
            patch_artist=self.patch_artist,
            widths=self.widths,
            positions=self.positions,
            showmeans=self.showmeans,
            showcaps=self.showcaps,
            showbox=self.showbox,
            showfliers=self.showfliers,
            boxprops=self.boxprops,
            medianprops=self.medianprops,
            flierprops=self.flierprops,
            whiskerprops=self.whiskerprops,
            capprops=self.capprops,
            meanprops=self.meanprops,
            labels=labels  # tự lấy từ dict key
        )

        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        fig.tight_layout()

        return fig