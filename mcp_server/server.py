from mcp.server.fastmcp import FastMCP
from service.order_dataset_service import get_all_orders as service_get_all_orders
from chart.barchart import BarChart
from chart.linechart import LineChart
from chart.distributionchart import DistributionChart
from chart.boxplotchart import BoxPlotChart
from chart.piechart import PieChart
from chart.barhorizontalchart import BarhChart
from chart.stackplotchart import StackPlotChart
from chart.violinchart import ViolinPlotChart
from chart.scatterchart import ScatterChart
import io
from typing import List, Union, Optional, Dict, Tuple, Callable
import matplotlib.colors as mcolors

mcp = FastMCP("Thanh server")

@mcp.tool()
def draw_bar_chart(x_data: List[Union[str, int, float]], y_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
                   type: str = "simple") -> str:
    """
    Generate a bar chart from the given data and return it as a PNG byte string.

    Parameters:
        x_data (list): A list of categories or labels for the x-axis.
        y_data (dict[str, list]): A dictionary where keys are labels and values are lists of numerical values.
        title (str): The title of the chart (default is an empty string).
        x_label (str): The label for the x-axis (default is an empty string).
        y_label (str): The label for the y-axis (default is an empty string).
        color (str): The color of the bars in the chart (default is "skyblue").
        type (str): The type of bar chart to create ("simple", "grouped" or "stacked"). If "grouped" or "stacked", y_data should be a list of lists.

    Returns:
        str: A base64-encoded PNG image of the generated bar chart.
    """
    bar_chart_object = BarChart(title = title, x_label = x_label, y_label = y_label, color = color, type = type)
    fig = bar_chart_object.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()

@mcp.tool()
def draw_barh_chart(category: Optional[Dict[str, List[Union[int, float]]]] = None,
                    data: Optional[List[Union[int, float]]] = None,
                    title: str = "",
                    x_label: str = "",
                    y_label: str = "",
                    color: Optional[Union[str, List[str]]] = None,
                    height: float = 0.8,
                    align: str = "center",
                    left: Optional[float] = None) -> str:
    """
    Generate a horizontal bar chart (barh) and return it as a base64-encoded PNG image.

    Parameters:
        category (dict, optional): A dictionary mapping category names to numeric values for grouped bar charts.
        data (list, optional): A list of numeric values for a simple bar chart (used if `category` is not provided).
        title (str): The title of the chart (default is "").
        x_label (str): The label for the x-axis (default is "").
        y_label (str): The label for the y-axis (default is "").
        color (str or list, optional): A single color or a list of colors for the bars (default is None).
        height (float): The height of each bar (default is 0.8).
        align (str): Bar alignment, either "center" or "edge" (default is "center").
        left (float, optional): The starting position of the bars on the x-axis (default is None).

    Returns:
        str: A base64-encoded PNG image of the horizontal bar chart.
    """
    if category:
        chart = BarhChart(title=title, x_label=x_label, y_label=y_label, color=color,
                          height=height, align=align, category=category, left=left)
    elif data:
        chart = BarhChart(title=title, x_label=x_label, y_label=y_label, color=color,
                          height=height, align=align, left=left)
    else:
        raise ValueError("Either 'category' or 'data' must be provided.")

    fig = chart.create_chart(data if not category else None)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

@mcp.tool()
def draw_boxplot_chart(data: Dict[str, List[float]], title: str = "", x_label: str = "", y_label: str = "",
                       notch: bool = False, vert: bool = True, showmeans: bool = False,
                       showcaps: bool = True, showbox: bool = True, showfliers: bool = True,
                       widths: Optional[List[float]] = None, positions: Optional[List[int]] = None, 
                       ) -> str:
    """
    Generate a boxplot chart from the given data and return it as a base64-encoded PNG string.

    Parameters:
        data (list of lists): A list of lists where each sublist represents a group of numeric values for the boxplot.
        title (str): The title of the chart.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        notch (bool): Whether to draw a notch in the boxplot (default is False).
        vert (bool): Whether the boxplot should be vertical (True) or horizontal (False, default is True).
        showmeans (bool): Whether to display the mean in the boxplot (default is False).
        showcaps (bool): Whether to display the caps at the ends of the whiskers (default is True).
        showbox (bool): Whether to display the box in the boxplot (default is True).
        showfliers (bool): Whether to display the outliers in the boxplot (default is True).
        widths (Optional[List[float]]): Width of the boxes in the boxplot (default is None).
        positions (Optional[List[int]]): Positions of the boxes along the x-axis (default is None).
        labels (Optional[List[str]]): Labels for each group in the boxplot (default is None).

    Returns:
        str: A base64-encoded PNG image of the generated boxplot.
    """
    chart = BoxPlotChart(
        title=title, x_label=x_label, y_label=y_label,
        notch=notch, vert=vert, showmeans=showmeans,
        showcaps=showcaps, showbox=showbox, showfliers=showfliers,
        widths=widths, positions=positions, labels=labels
    )
    fig = chart.create_chart(data)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf.read()

@mcp.tool()
def draw_distribution_chart(category: Optional[Dict[str, List[Union[int, float]]]] = None, 
                            data: Optional[List[Union[int, float]]] = None, 
                            bins: int = 10, title: str = "", 
                            x_label: str = "", y_label: str = "", 
                            color: Optional[Union[str, List[str]]] = None, 
                            alpha: float = 0.75, stacked: bool = False) -> str:
    """
    Generate a histogram (distribution chart) from the given data and return it as a base64-encoded PNG string.

    Parameters:
        category (dict): A dictionary where keys are categories and values are lists of numeric values for each group.
        data (list): A list of numeric values for a single dataset (if category is not provided).
        bins (int): The number of histogram bins (default is 10).
        title (str): The title of the chart.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        color (Optional[str or list]): The color of the bars (default is None). Can be a single color or a list of colors.
        alpha (float): The transparency of the bars (default is 0.75).
        stacked (bool): Whether the bars should be stacked (default is False).

    Returns:
        str: A base64-encoded PNG image of the generated histogram.
    """
    if category:
        chart = DistributionChart(
            title=title, x_label=x_label, y_label=y_label, color=color, bins=bins,
            alpha=alpha, category=category, stacked=stacked
        )
    elif data:
        chart = DistributionChart(
            title=title, x_label=x_label, y_label=y_label, color=color, bins=bins,
            alpha=alpha, stacked=stacked
        )
    else:
        raise ValueError("Either 'category' or 'data' must be provided.")

    fig = chart.create_chart(data if not category else None)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

@mcp.tool()
def draw_line_chart(x: List[Union[int, float]], y: List[Union[int, float]], title: str = "", x_label: str = "", y_label: str = "",
                    linestyle: str = "-", linewidth: float = 2, marker: Optional[str] = None,
                    color: Optional[str] = None, scalex: bool = True, scaley: bool = True,
                    label: Optional[str] = None) -> str:
    """
    Generate a line chart from the given x and y data and return it as a PNG byte string.

    Parameters:
        x (list): A list of numerical values for the x-axis.
        y (list): A list of numerical values for the y-axis.
        title (str): The title of the chart (default is an empty string).
        x_label (str): The label for the x-axis (default is an empty string).
        y_label (str): The label for the y-axis (default is an empty string).
        linestyle (str): The style of the line (default is solid line, "-").
        linewidth (float): The thickness of the line (default is 2).
        marker (Optional[str]): The marker to use for data points (default is None).
        color (Optional[str]): The color of the line (default is None, which uses the default color).
        scalex (bool): Whether to scale the x-axis (default is True).
        scaley (bool): Whether to scale the y-axis (default is True).
        label (Optional[str]): The label for the legend (default is None).

    Returns:
        str: A base64-encoded PNG image of the generated line chart.
    """
    chart = LineChart(
        title=title, x_label=x_label, y_label=y_label,
        linestyle=linestyle, linewidth=linewidth, marker=marker,
        color=color, scalex=scalex, scaley=scaley, label=label
    )
    fig = chart.create_chart(x, y)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf.read()

@mcp.tool()
def draw_pie_chart(x: List[Union[int, float]], labels: Optional[List[str]] = None, explode: Optional[List[float]] = None,
                   colors: Optional[List[str]] = None, autopct: Optional[str] = None, pctdistance: float = 0.6, 
                   shadow: bool = False, labeldistance: float = 1.1, startangle: float = 0, radius: float = 1, 
                   counterclock: bool = True, center: List[float] = [0, 0], frame: bool = False, 
                   rotatelabels: bool = False, normalize: bool = True, title: str = "") -> str:
    """
    Generate a pie chart from the given data and return it as a base64-encoded PNG string.

    Parameters:
        x (list): A list of numerical values for the pie chart (sizes of each slice).
        labels (Optional[list]): A list of labels for each slice (default is None).
        explode (Optional[list]): A list specifying the fraction of the radius to offset each slice (default is None).
        colors (Optional[list]): A list of colors for each slice (default is None).
        autopct (Optional[str]): String format for percentage display (default is None).
        pctdistance (float): Distance between the center and the labels in the pie chart (default is 0.6).
        shadow (bool): Whether to display a shadow behind the pie chart (default is False).
        labeldistance (float): Distance between the center and the labels (default is 1.1).
        startangle (float): The angle by which to rotate the start of the pie chart (default is 0).
        radius (float): The radius of the pie chart (default is 1).
        counterclock (bool): Whether to draw the pie chart counterclockwise (default is True).
        center (tuple): A tuple specifying the x, y position of the pie chart (default is (0, 0)).
        frame (bool): Whether to draw a frame around the pie chart (default is False).
        rotatelabels (bool): Whether to rotate the labels to match the slice angle (default is False).
        normalize (bool): Whether to normalize the data (default is True).
        title (str): The title of the pie chart (default is "").

    Returns:
        str: A base64-encoded PNG image of the pie chart.
    """
    chart = PieChart(
        explode=explode, labels=labels, colors=colors, autopct=autopct, pctdistance=pctdistance,
        shadow=shadow, labeldistance=labeldistance, startangle=startangle, radius=radius,
        counterclock=counterclock, center=center, frame=frame, rotatelabels=rotatelabels,
        normalize=normalize, title=title
    )

    fig = chart.create_chart(x)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()

@mcp.tool()
def draw_scatter_chart(
    x: List[float],
    y: List[float],
    s: List[float] = [],
    c: List[Union[float, str]] = [],
    marker: str = 'o',
    cmap: str = "",
    norm = None,  # ← Thêm dòng này lại
    vmin: float = 0.0,
    vmax: float = 1.0,
    alpha: float = 1.0,
    linewidths: float = 0.5,
    edgecolors: str = 'face',
    colorizer = None,
    plotnonfinite: bool = False,
    title: str = ""
) -> str:
    """
    Generate a scatter plot using the provided x and y values with customizable visual attributes.

    Parameters:
        x (List[float]): X-axis values of the scatter points.
        y (List[float]): Y-axis values of the scatter points.
        s (List[float], optional): Sizes of each point.
        c (List[float] or List[str], optional): Colors of each point (numeric or string colors).
        marker (str): Style of point markers (default: 'o').
        cmap (str or Colormap, optional): Colormap used if `c` is numeric.
        norm (Normalize, optional): Normalize instance to scale colormap.
        vmin (float, optional): Minimum value for colormap normalization.
        vmax (float, optional): Maximum value for colormap normalization.
        alpha (float, optional): Opacity level of points (0 to 1).
        linewidths (float, optional): Width of point edges.
        edgecolors (str, optional): Edge color for points.
        colorizer (Callable, optional): Custom function to apply color logic.
        plotnonfinite (bool): Whether to plot NaN/inf points (default: False).
        title (str): Title of the chart.

    Returns:
        str: Base64-encoded PNG image of the scatter plot.
    """
    chart = ScatterChart(
        x=x,
        y=y,
        s=s,
        c=c,
        marker=marker,
        cmap=cmap,
        norm=norm,
        vmin=vmin,
        vmax=vmax,
        alpha=alpha,
        linewidths=linewidths,
        edgecolors=edgecolors,
        colorizer=colorizer,
        plotnonfinite=plotnonfinite,
        title=title
    )

    fig = chart.create_chart()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()

@mcp.tool()
def draw_stackplot_chart(category: Dict[str, List[Union[int, float]]],
                         x: List[Union[int, float]],
                         title: str = "",
                         x_label: str = "",
                         y_label: str = "",
                         colors: Optional[List[str]] = None,
                         baseline: str = "zero",
                         hatch: Optional[List[str]] = None) -> str:
    """
    Generate a stacked area chart (stackplot) from the given category data and return it as a base64-encoded PNG image.

    Parameters:
        category (dict): A dictionary mapping labels to lists of y-values (e.g., {"Group A": [...], "Group B": [...]}).
        x (list): List of x-values shared by all series.
        title (str): The title of the chart (default is "").
        x_label (str): The label for the x-axis (default is "").
        y_label (str): The label for the y-axis (default is "").
        colors (list, optional): List of colors for the filled areas (default is None).
        baseline (str): Baseline style; options include "zero", "sym", "wiggle", "weighted_wiggle" (default is "zero").
        hatch (list, optional): List of hatch patterns for each area fill (default is None).

    Returns:
        str: A base64-encoded PNG image of the stacked area chart.
    """
    chart = StackPlotChart(title=title, x_label=x_label, y_label=y_label,
                           colors=colors, baseline=baseline, hatch=hatch, category=category)
    fig = chart.create_chart(x)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

@mcp.tool()
def draw_violinplot_chart(category: Dict[str, List[Union[int, float]]],
                          title: str = "",
                          x_label: str = "",
                          y_label: str = "",
                          orientation: str = "vertical",
                          widths: float = 0.5,
                          showmeans: bool = False,
                          showextrema: bool = True,
                          showmedians: bool = False,
                          quantiles: Optional[List[float]] = None,
                          points: int = 100,
                          bw_method: Optional[Union[str, float]] = None,
                          side: str = "both") -> str:
    """
    Generate a violin plot from the given category data and return it as a base64-encoded PNG image.

    Parameters:
        category (dict): A dictionary where keys are category labels and values are lists of numeric data.
        title (str): Title of the plot (default is "").
        x_label (str): Label for the x-axis (default is "").
        y_label (str): Label for the y-axis (default is "").
        orientation (str): "vertical" or "horizontal" (default is "vertical").
        widths (float): Width of the violins (default is 0.5).
        showmeans (bool): Whether to show the mean line (default is False).
        showextrema (bool): Whether to show min/max lines (default is True).
        showmedians (bool): Whether to show the median line (default is False).
        quantiles (list, optional): Quantiles to display inside the violin (e.g., [0.25, 0.5, 0.75]).
        points (int): Number of evaluation points per violin (default is 100).
        bw_method (str or float, optional): Method used to calculate the estimator bandwidth.
        side (str): "both", "left", or "right" (only applies to horizontal plots in some backends).

    Returns:
        str: A base64-encoded PNG image of the violin plot.
    """
    chart = ViolinPlotChart(
        title=title,
        x_label=x_label,
        y_label=y_label,
        orientation=orientation,
        widths=widths,
        showmeans=showmeans,
        showextrema=showextrema,
        showmedians=showmedians,
        quantiles=quantiles,
        points=points,
        bw_method=bw_method,
        side=side,
        category=category
    )

    fig = chart.create_chart()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()


if __name__ == "__main__":
    # Register the service with the server
    mcp.run(transport="sse")