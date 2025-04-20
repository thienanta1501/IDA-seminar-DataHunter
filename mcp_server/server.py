from mcp.server.fastmcp import FastMCP
from service.order_dataset_service import get_all_orders as service_get_all_orders
from chart.barchart import BarChart
from chart.linechart import LineChart
from chart.histchart import DistributionChart
from chart.boxplotchart import BoxPlotChart
from chart.piechart import PieChart
from chart.barhorizontalchart import BarhChart
from chart.stackplotchart import StackPlotChart
from chart.violinchart import ViolinPlotChart
from chart.scatterchart import ScatterChart
import io

mcp = FastMCP("Thanh server")

@mcp.tool()
def draw_bar_chart(x_data: list, y_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
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
def draw_line_chart(x_data: list, y_data: list, title: str = "", x_label: str = "", y_label: str = "", color: str = "blue") -> str:
    """
    Generate a line chart from the given data and return it as a PNG byte string.

    Parameters:
        x_data (list): A list of categories or labels for the x-axis.
        y_data (list): A list of numerical values corresponding to each x-axis label.
        title (str): The title of the chart (default is an empty string).
        x_label (str): The label for the x-axis (default is an empty string).
        y_label (str): The label for the y-axis (default is an empty string).
        color (str): The color of the line in the chart (default is "blue").

    Returns:
        str: A base64-encoded PNG image of the generated line chart.
    """
    line_chart_object = LineChart(title = title, x_label = x_label, y_label = y_label, color = color)
    fig = line_chart_object.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

@mcp.tool()
def draw_distribution_chart(category: dict = None, data: list = None, bins: int = 10, title: str = "", 
                            x_label: str = "", y_label: str = "", color=None, alpha: float = 0.75, stacked: bool = False) -> str:
    """
    Generate a histogram (distribution chart) from the given data and return it as a base64-encoded PNG string.

    Parameters:
        category (dict): A dictionary of categories with lists of numeric values for each group.
        data (list): A list of numeric values for single dataset (if category is not provided).
        bins (int): Number of histogram bins (default is 10).
        title (str): Chart title.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        color (str or list): Bar color (default is green). Can be a single color or a list of colors.
        alpha (float): The transparency of the bars (default 0.75).
        stacked (bool): Whether the bars should be stacked (default False).

    Returns:
        str: A base64-encoded PNG image of the histogram.
    """
    if category:
        chart = DistributionChart(title=title, x_label=x_label, y_label=y_label, color=color, bins=bins,
                                  alpha=alpha, category=category, stacked=stacked)
    elif data:
        chart = DistributionChart(title=title, x_label=x_label, y_label=y_label, color=color, bins=bins,
                                  alpha=alpha, stacked=stacked)
    else:
        raise ValueError("Either 'category' or 'data' must be provided.")

    fig = chart.create_chart(data if not category else None)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

@mcp.tool()
def draw_box_plot(data: list, title: str = "", x_label: str = "", y_label: str = "", color: str = "blue") -> str:
    """
    Generate a box plot from the given data and return it as a PNG byte string.

    Parameters:
        data (list): A list of numeric values for the box plot.
        title (str): Chart title.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        color (str): Box color (default is blue).

    Returns:
        str: A base64-encoded PNG image of the box plot.
    """
    chart = BoxPlotChart(title=title, x_label=x_label, y_label=y_label, color=color)
    fig = chart.create_chart(data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()


@mcp.tool()
def draw_pie_chart(labels: list, values: list, title: str = "", colors: list = None) -> str:
    """
    Generate a pie chart from the given data and return it as a PNG byte string.

    Parameters:
        labels (list): A list of category labels for the pie chart.
        values (list): A list of numerical values for each category.
        title (str): Title of the chart.
        colors (list): Optional list of colors for each slice.

    Returns:
        str: A base64-encoded PNG image of the pie chart.
    """
    chart = PieChart(title=title, colors=colors)
    fig = chart.create_chart(labels, values)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

@mcp.tool()
def draw_barh_chart(category: dict = None, data: list = None, title: str = "", 
                    x_label: str = "", y_label: str = "", color=None,
                    height: float = 0.8, align: str = "center", left: float = None) -> str:
    """
    Generate a horizontal bar chart and return it as a base64-encoded PNG string.

    Parameters:
        category (dict): Dictionary of categories with numeric values.
        data (list): List of numeric values if no category is provided.
        color (str or list): Color(s) of the bars.
        height (float): Height of each bar (default 0.8).
        align (str): Alignment of bars, 'center' or 'edge'.
        left (float): Starting position of bars (default None).

    Returns:
        str: Base64-encoded PNG image.
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
def draw_stackplot_chart(category: dict, x: list, title: str = "", 
                         x_label: str = "", y_label: str = "", colors=None,
                         baseline: str = "zero", hatch=None) -> str:
    """
    Generate a stackplot from the given category data and return it as a base64-encoded PNG string.

    Parameters:
        category (dict): Dictionary with keys as labels and values as list of y-values.
        x (list): List of x-values corresponding to each y-series.
        colors (list): List of colors for each area.
        baseline (str): Baseline method (e.g., 'zero', 'sym', 'wiggle', 'weighted_wiggle').

    Returns:
        str: Base64-encoded PNG image of the stackplot.
    """
    chart = StackPlotChart(title=title, x_label=x_label, y_label=y_label,
                           colors=colors, baseline=baseline, hatch=hatch, category=category)
    fig = chart.create_chart(x)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()


@mcp.tool()
def draw_violinplot_chart(category: dict, title: str = "", x_label: str = "", y_label: str = "",
                          orientation: str = "vertical", widths: float = 0.5, showmeans: bool = False,
                          showextrema: bool = True, showmedians: bool = False, quantiles=None,
                          points: int = 100, bw_method=None, side: str = "both") -> str:
    """
    Generate a violin plot from the given category data and return it as a base64-encoded PNG string.
    """
    chart = ViolinPlotChart(
        title=title, x_label=x_label, y_label=y_label,
        orientation=orientation, widths=widths, showmeans=showmeans,
        showextrema=showextrema, showmedians=showmedians,
        quantiles=quantiles, points=points, bw_method=bw_method,
        side=side, category=category
    )

    fig = chart.create_chart()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()


@mcp.tool()
def draw_scatter_chart(x_data: list, y_data: list, title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue") -> str:
    """
    Generate a scatter chart from the given data and return it as a PNG byte string.

    Parameters:
        x_data (list): A list of categories or labels for the x-axis.
        y_data (list): A list of numerical values corresponding to each x-axis label.
        title (str): The title of the chart (default is an empty string).
        x_label (str): The label for the x-axis (default is an empty string).
        y_label (str): The label for the y-axis (default is an empty string).
        color (str): The color of the points in the chart (default is "skyblue").

    Returns:
        str: A base64-encoded PNG image of the generated scatter chart.
    """
    scatter_chart_object = ScatterChart(title=title, x_label=x_label, y_label=y_label, color=color)
    fig = scatter_chart_object.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

if __name__ == "__main__":
    # Register the service with the server
    mcp.run(transport="sse")