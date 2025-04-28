import matplotlib.pyplot as plt

class PieChart:
    def __init__(self, explode=None, labels=None, colors=None, autopct=None, pctdistance=0.6,
                 shadow=False, labeldistance=1.1, startangle=0, radius=1, counterclock=True,
                 wedgeprops=None, textprops=None, center=(0, 0), frame=False,
                 rotatelabels=False, normalize=True, hatch=None, title=""):
        self.explode = explode
        self.labels = labels
        self.colors = colors
        self.autopct = '%1.1f%%' if autopct is None else autopct
        self.pctdistance = pctdistance
        self.shadow = shadow
        self.labeldistance = labeldistance
        self.startangle = startangle
        self.radius = radius
        self.counterclock = counterclock
        self.wedgeprops = wedgeprops
        self.textprops = textprops
        self.center = center
        self.frame = frame
        self.rotatelabels = rotatelabels
        self.normalize = normalize
        self.hatch = hatch
        self.title = title

    def create_chart(self, x):
        fig, ax = plt.subplots()

        wedges, texts, autotexts = ax.pie(
            x,
            explode=self.explode,
            labels=self.labels,
            colors=self.colors,
            autopct=self.autopct,
            pctdistance=self.pctdistance,
            shadow=self.shadow,
            labeldistance=self.labeldistance,
            startangle=self.startangle,
            radius=self.radius,
            counterclock=self.counterclock,
            wedgeprops=self.wedgeprops,
            textprops=self.textprops,
            center=self.center,
            frame=self.frame,
            rotatelabels=self.rotatelabels,
            normalize=self.normalize,
            hatch=self.hatch
        )

        for autotext in autotexts:
            autotext.set_color('white')

        ax.set_title(self.title)
        return fig