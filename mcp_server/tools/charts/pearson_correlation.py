import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class PearsonCorrelation:
    def __init__(self, title: str = ""):
        self.title = title

    def create_chart(self, data: dict[str, list]):
        fig, ax = plt.subplots(figsize=(8, 6))
        df = pd.DataFrame(data)
        corr = df.corr(method="pearson")

        sns.heatmap(
            corr,
            annot=True,
            cmap='coolwarm',
            fmt=".2f",
            vmin=-1, vmax=1,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax  
        )

        ax.set_title(self.title, fontsize=16)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=10 ,ha='right')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

        fig.tight_layout()

        return fig