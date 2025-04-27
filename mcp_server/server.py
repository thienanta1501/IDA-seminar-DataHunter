from mcp.server.fastmcp import FastMCP
from service.order_dataset_service import get_all_orders as service_get_all_orders
from chart.arrowchart import ArrowChart
from chart.barchart import BarChart
from chart.barhorizontalchart import BarhChart
from chart.boxplotchart import BoxPlotChart
from chart.distributionchart import DistributionChart
from chart.errorbarchart import ErrorBarChart
from chart.fillbetweenchart import FillBetweenChart
from chart.fillbetweenxchart import FillBetweenXChart
from chart.linechart import LineChart
from chart.piechart import PieChart
from chart.polarchart import PolarChart
from chart.quiverchart import QuiverChart
from chart.scatterchart import ScatterChart
from chart.stackplotchart import StackPlotChart
from chart.stemchart import StemChart
from chart.stepchart import StepChart
from chart.violinchart import ViolinPlotChart

import io
from typing import List, Union, Optional, Dict, Tuple, Callable
import os
from dotenv import load_dotenv
import matplotlib.colors as mcolors
import numpy as np
from utils.index import upload_image_to_imgur

load_dotenv()

client_id = os.getenv("CLIENT_ID")
image_host_url = os.getenv("IMAGE_HOST_SERVER_URL")

mcp = FastMCP("Thanh server")

@mcp.tool()
def draw_arrow_chart(x: float, y: float, dx: float, dy: float,
                     title: str = "", x_label: str = "", y_label: str = "",
                     color: str = "blue", width: float = 0.01,
                     head_width: float = 0.05, head_length: float = 0.1,
                     length_includes_head: bool = True) -> str:
    """
    Generate a chart with an arrow and return it as a base64-encoded PNG string.
    
    Parameters
    ----------
    x, y : float
        Starting point of the arrow.
    dx, dy : float
        Direction and length of the arrow.
    title, x_label, y_label : str, optional
        Title and axis labels for the chart.
    color : str, optional
        Arrow color.
    width : float, optional
        Width of the arrow body.
    head_width : float, optional
        Width of the arrow head.
    head_length : float, optional
        Length of the arrow head.
    length_includes_head : bool, optional
        Whether the head length is included in total arrow length.

    Returns
    -------
    str
        A URL string linking to the generated arrow chart image hosted online.
    """
    chart = ArrowChart(title=title, x_label=x_label, y_label=y_label,
                       color=color, width=width,
                       head_width=head_width, head_length=head_length,
                       length_includes_head=length_includes_head)
    fig = chart.create_chart(x, y, dx, dy)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_bar_chart(x_data: List[Union[str, int, float]], y_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
                   type: str = "simple") -> str:
    """
    Draws a bar chart based on the provided data and returns the image as a hosted URL.

    Parameters
    ----------
    x_data : list of str | int | float
        A list of category labels for the x-axis.

    y_data : dict[str, list]
        A dictionary containing one or more data series:
            - Keys are the series names (e.g., "Revenue", "Profit").
            - Values are lists of numerical values aligned with `x_data`.

    title : str, optional
        The title of the chart. Default is an empty string.

    x_label : str, optional
        The label for the x-axis. Default is an empty string.

    y_label : str, optional
        The label for the y-axis. Default is an empty string.

    color : str, optional
        The color of the bars. Applies only to simple charts or all series if using a single color. Default is "skyblue".

    type : str, optional
        The type of bar chart to create. Options include:
            - "simple": A basic single-series bar chart.
            - "grouped": A grouped bar chart for comparing multiple series side-by-side.
            - "stacked": A stacked bar chart combining multiple series.
        If multiple series are provided and `type` is not explicitly set, it defaults to "stacked".

    Returns
    -------
    str
        A URL string linking to the generated bar chart image hosted online.
    """

    bar_chart_object = BarChart(title = title, x_label = x_label, y_label = y_label, color = color, type = type)
    fig = bar_chart_object.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link


@mcp.tool()
def draw_barh_chart(y_data: List[Union[str, int, float]], x_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
                   type: str = "simple") -> str:
    """
    Generate a horizontal bar chart and return it as a PNG byte string.

    This function uses the BarhChart class to generate a horizontal bar chart based on the given data.
    It supports "simple", "grouped", and "stacked" chart types.

    Parameters
    ----------
    y_data : list of str | int | float
        A list of labels for the y-axis categories (e.g., names, groups, etc.).
    x_data : dict of str -> list of float
        A dictionary where keys are data series labels and values are lists of numerical values
        corresponding to each y-axis label in `y_data`.
    title : str, optional
        The title of the chart (default is an empty string).
    x_label : str, optional
        The label for the x-axis (default is an empty string).
    y_label : str, optional
        The label for the y-axis (default is an empty string).
    color : str, optional
        The default color for bars (only applies to "simple" charts). Default is "skyblue".
    type : str, optional
        Type of bar chart to draw. One of:
            - "simple": A basic horizontal bar chart using the first series in `x_data`.
            - "grouped": Displays bars for each series side by side.
            - "stacked": Stacks values of all series on the same bar.
        Default is "simple".

    Returns
    -------
    str
        A URL string linking to the generated bar horizontal chart image hosted online.
    """

    bar_chart_object = BarhChart(title = title, x_label = x_label, y_label = y_label, color = color, type = type)
    fig = bar_chart_object.create_chart(y_data_labels=y_data, x_data_dict=x_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_boxplot_chart(data: Dict[str, List[float]], title: str = "", x_label: str = "", y_label: str = "",
                       notch: bool = False, vert: bool = True, showmeans: bool = False,
                       showcaps: bool = True, showbox: bool = True, showfliers: bool = True,
                       widths: Optional[List[float]] = None, positions: Optional[List[int]] = None, 
                       ) -> str:
    """
    Generate a boxplot chart from the given data and return it as a base64-encoded PNG string.

    Parameters:
        data (Dict[str, List[float]]): A dictionary where each key is a label (str) for a data group, 
        and the value is a list of float numbers representing the numeric values in that group.
        Each key corresponds to one box in the boxplot.
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
        A URL string linking to the generated boxplot image hosted online.
    """
    chart = BoxPlotChart(
        title=title, x_label=x_label, y_label=y_label,
        notch=notch, vert=vert, showmeans=showmeans,
        showcaps=showcaps, showbox=showbox, showfliers=showfliers,
        widths=widths, positions=positions
    )
    fig = chart.create_chart(data)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

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
        A URL string linking to the generated distribution chart image hosted online.
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

    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_error_bar_chart(x_data: List[Union[int, float]],
                         y_data: List[Union[int, float]],
                         yerr: Optional[Union[float, List[float]]] = None,
                         xerr: Optional[Union[float, List[float]]] = None,
                         title: str = "", x_label: str = "", y_label: str = "",
                         fmt: str = "o", color: Optional[str] = None, ecolor: Optional[str] = None,
                         elinewidth: Optional[float] = None, capsize: Optional[float] = None,
                         barsabove: bool = False, errorevery: int = 1,
                         capthick: Optional[float] = None) -> str:
    """
    Plots an error bar chart using the provided x and y data, with optional error bars
    for both x and y axes, and uploads the generated chart image to Imgur.

    Args:
        x_data (List[Union[int, float]]): The data for the x-axis.
        y_data (List[Union[int, float]]): The data for the y-axis.
        yerr (Optional[Union[float, List[float]]], optional): The y-axis error values. Default is None.
        xerr (Optional[Union[float, List[float]]], optional): The x-axis error values. Default is None.
        title (str, optional): The title of the chart. Default is an empty string.
        x_label (str, optional): The label for the x-axis. Default is an empty string.
        y_label (str, optional): The label for the y-axis. Default is an empty string.
        fmt (str, optional): The format of the plot markers and lines. Default is "o".
        color (Optional[str], optional): The color of the markers and lines. Default is None.
        ecolor (Optional[str], optional): The color of the error bars. Default is None.
        elinewidth (Optional[float], optional): The line width of the error bars. Default is None.
        capsize (Optional[float], optional): The size of the caps at the ends of the error bars. Default is None.
        barsabove (bool, optional): If True, draws error bars above the data points. Default is False.
        errorevery (int, optional): Specifies the step size for drawing error bars. Default is 1.
        capthick (Optional[float], optional): The thickness of the caps on the error bars. Default is None.

    Returns:
        str: The URL link of the uploaded error bar chart image on Imgur.

    Example:
        >>> draw_error_bar_chart([1, 2, 3], [2, 3, 4], yerr=[0.1, 0.2, 0.3])
        'https://imgur.com/your-uploaded-image-link'

    """
    chart = ErrorBarChart(title=title, x_label=x_label, y_label=y_label,
                          fmt=fmt, color=color, ecolor=ecolor,
                          elinewidth=elinewidth, capsize=capsize,
                          barsabove=barsabove, errorevery=errorevery,
                          capthick=capthick)
    fig = chart.create_chart(x_data, y_data, yerr, xerr)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_fill_between_chart(x_data: List[Union[str, int, float]],
                            y1_data: List[Union[int, float]],
                            y2_data: Union[List[Union[int, float]], int, float] = 0,
                            where: Optional[List[bool]] = None,
                            title: str = "", x_label: str = "", y_label: str = "",
                            color: str = "blue", alpha: float = 0.5,
                            step: Optional[str] = None, interpolate: bool = False) -> str:
    """
    Plots a filled area chart between two y datasets (y1 and y2) over the provided x data, 
    with optional customization for color, transparency, and step formatting, 
    and uploads the generated chart image to Imgur.

    Args:
        x_data (List[Union[str, int, float]]): The data for the x-axis. Can be integers, floats, or strings.
        y1_data (List[Union[int, float]]): The first set of data for the y-axis.
        y2_data (Union[List[Union[int, float]], int, float], optional): The second set of data for the y-axis (or a constant value). Default is 0.
        where (Optional[List[bool]], optional): A boolean list indicating where to fill the area. Default is None.
        title (str, optional): The title of the chart. Default is an empty string.
        x_label (str, optional): The label for the x-axis. Default is an empty string.
        y_label (str, optional): The label for the y-axis. Default is an empty string.
        color (str, optional): The color of the filled area. Default is "blue".
        alpha (float, optional): The transparency level of the filled area. Default is 0.5.
        step (Optional[str], optional): If "pre", "post", or "mid", creates a step chart instead of a continuous line. Default is None.
        interpolate (bool, optional): If True, interpolate the data between points. Default is False.

    Returns:
        str: The URL link of the uploaded filled area chart image on Imgur.

    Example:
        >>> draw_fill_between_chart([1, 2, 3], [2, 3, 4], y2_data=[1, 2, 3])
        'https://imgur.com/your-uploaded-image-link'

    """
    chart = FillBetweenChart(title=title, x_label=x_label, y_label=y_label, color=color,
                             alpha=alpha, step=step, interpolate=interpolate)
    fig = chart.create_chart(x_data, y1_data, y2_data, where)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_fill_betweenx_chart(y: List[Union[int, float]],
                             x1: List[Union[int, float]],
                             x2: Union[List[Union[int, float]], float] = 0,
                             where: Union[List[bool], None] = None,
                             title: str = "", x_label: str = "", y_label: str = "",
                             color: str = "blue", alpha: float = 0.5,
                             step: str = None, interpolate: bool = False) -> str:
    """
    Generate a filled area chart between two x-values over the y-axis and return it as a base64-encoded PNG string.

    Parameters
    ----------
    y : list
        Y-axis values.
    x1 : list
        First set of x-values (left or right edge).
    x2 : list or float, optional
        Second set of x-values (default is 0).
    where : list of bool, optional
        Condition to apply fill (e.g. x1 > x2).
    title, x_label, y_label : str
        Chart title and axis labels.
    color : str, optional
        Fill color.
    alpha : float, optional
        Transparency of the fill.
    step : str, optional
        Step fill direction: 'pre', 'mid', or 'post'.
    interpolate : bool, optional
        Whether to interpolate when using `where`.

    Returns:
        str: The URL link of the uploaded filled area chart image on Imgur.

    Example:
        >>> draw_fill_between_chart([1, 2, 3], [2, 3, 4], y2_data=[1, 2, 3])
        'https://imgur.com/your-uploaded-image-link'
    """
    chart = FillBetweenXChart(title=title, x_label=x_label, y_label=y_label,
                              color=color, alpha=alpha, step=step, interpolate=interpolate)
    fig = chart.create_chart(y=y, x1=x1, x2=x2, where=where)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_line_chart(x_data: List[Union[str, int, float]] , y_data: Dict[Union[str], List[Union[float, int]]], title: str = "", x_label: str = "", y_label: str = "",
                    linestyle: str = "-", linewidth: float = 2, marker: Optional[str] = None,
                    color: Optional[str] = None, scalex: bool = True, scaley: bool = True) -> str:
    """
    Draws a multi-line chart using the given x-axis values and multiple y-axis data series,
    and returns the chart image as a PNG binary string.

    Args:
        x_data (List[Union[str, int, float]]): 
            Values for the x-axis (shared by all lines).
        y_data (Dict[Union[str], List[Union[float, int]]]): 
            Dictionary mapping labels to y-axis values for each line to be plotted.
            Each key is a line label, and each value is a list of y-values corresponding to x_data.
        title (str, optional): 
            Title of the chart.
        x_label (str, optional): 
            Label for the x-axis.
        y_label (str, optional): 
            Label for the y-axis.
        linestyle (str, optional): 
            Line style (default is '-', a solid line).
        linewidth (float, optional): 
            Width of the lines.
        marker (Optional[str], optional): 
            Marker style for data points (e.g., 'o', 's', '^').
        color (Optional[str], optional): 
            Color or list of colors for each line.
        scalex (bool, optional): 
            Whether to auto-scale the x-axis.
        scaley (bool, optional): 
            Whether to auto-scale the y-axis.

    Returns:
        A URL string linking to the generated line chart image hosted online.
    """
    chart = LineChart(
        title=title, x_label=x_label, y_label=y_label,
        linestyle=linestyle, linewidth=linewidth, marker=marker,
        color=color, scalex=scalex, scaley=scaley
    )
    fig = chart.create_chart(x_data=x_data, y_data=y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

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
        A URL string linking to the generated pie chart image hosted online.
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
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_polar_chart(theta_data: List[Union[int, float]], r_data: List[Union[int, float]],
                     title: str = "", color: str = "blue", linewidth: float = 1.5) -> str:
    """
    Plots a polar chart using the provided theta (angular) and r (radial) data, with optional 
    customization for the chart title, color, and line width, and uploads the generated chart image to Imgur.

    Args:
        theta_data (List[Union[int, float]]): The angular data for the chart (theta), typically in radians.
        r_data (List[Union[int, float]]): The radial data for the chart (r), representing the distance from the center.
        title (str, optional): The title of the chart. Default is an empty string.
        color (str, optional): The color of the plot lines. Default is "blue".
        linewidth (float, optional): The line width of the plot. Default is 1.5.

    Returns:
        str: The URL link of the uploaded polar chart image on Imgur.

    Example:
        >>> draw_polar_chart([0, 1, 2], [1, 2, 3], title="Polar Plot", color="red")
        'https://imgur.com/your-uploaded-image-link'

    """
    chart = PolarChart(title=title, color=color, linewidth=linewidth)
    fig = chart.create_chart(theta_data, r_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_quiver_chart(x_data: List[Union[int, float]], y_data: List[Union[int, float]],
                      u_data: List[Union[int, float]], v_data: List[Union[int, float]],
                      title: str = "", x_label: str = "", y_label: str = "",
                      color: str = "blue", scale: float = 1.0) -> str:
    """
    Plots a quiver chart using the provided x, y data and their corresponding vector components (u, v),
    with optional customization for the chart title, axis labels, color, and scale, 
    and uploads the generated chart image to Imgur.

    Args:
        x_data (List[Union[int, float]]): The x coordinates of the vector origins.
        y_data (List[Union[int, float]]): The y coordinates of the vector origins.
        u_data (List[Union[int, float]]): The x components of the vectors.
        v_data (List[Union[int, float]]): The y components of the vectors.
        title (str, optional): The title of the chart. Default is an empty string.
        x_label (str, optional): The label for the x-axis. Default is an empty string.
        y_label (str, optional): The label for the y-axis. Default is an empty string.
        color (str, optional): The color of the vectors. Default is "blue".
        scale (float, optional): The scaling factor for the vectors. Default is 1.0.

    Returns:
        str: The URL link of the uploaded quiver chart image on Imgur.

    Example:
        >>> draw_quiver_chart([1, 2, 3], [1, 2, 3], [0.5, -0.5, 0.2], [0.5, 0.5, -0.2], title="Quiver Plot", color="green")
        'https://imgur.com/your-uploaded-image-link'

    """
    chart = QuiverChart(title=title, x_label=x_label, y_label=y_label, color=color, scale=scale)
    fig = chart.create_chart(x_data, y_data, u_data, v_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_scatter_chart(
    x: List[float],
    y: List[float],
    s: Union[float, List[float]] = 20.0,  # Kích thước điểm, có thể là scalar hoặc array
    c: Union[float, str, List[Union[float, str]]]=[],  # Màu sắc điểm, có thể là scalar, string hoặc list
    marker: str = 'o',
    cmap: str = "",
    norm = None,
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
        s (float or List[float], optional): Size of points. Either a scalar or a list with the same length as x/y.
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
        A URL string linking to the generated scatter chart image hosted online.
    """
    # Ensure `s` is either a scalar or a list with the same length as x and y
    if isinstance(s, float):
        s = [s] * len(x)
    
    # Ensure `c` is either a list with the same length as x and y, or a valid color string
    if isinstance(c, (float, str)):  # If `c` is scalar or string, repeat for all points
        c = [c] * len(x)
    elif isinstance(c, list) and len(c) != len(x):  # If list, check length consistency
        if len(c) == 0:  # If `c` is an empty list, use default color
            c = ['blue'] * len(x)
        else:
            raise ValueError("The length of `c` must be the same as the length of `x` and `y`.")

    # Create the scatter plot chart
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

    # Generate the plot and save it to a buffer
    fig = chart.create_chart()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Return the base64-encoded PNG image as a string
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

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
        A URL string linking to the generated stackplot chart image hosted online.
    """
    chart = StackPlotChart(title=title, x_label=x_label, y_label=y_label,
                           colors=colors, baseline=baseline, hatch=hatch, category=category)
    fig = chart.create_chart(x)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_stem_chart(x_data: List[Union[str, int, float]], y_data: List[Union[int, float]],
                    title: str = "", x_label: str = "", y_label: str = "",
                    linefmt: str = "C0-", markerfmt: str = "C0o", basefmt: str = "k-",
                    bottom: float = 0, orientation: str = "vertical") -> str:
    """
    Plots a stem chart using the provided x and y data, with optional customization for 
    chart title, axis labels, line and marker formatting, and orientation, 
    and uploads the generated chart image to Imgur.

    Args:
        x_data (List[Union[str, int, float]]): The x coordinates of the stem chart.
        y_data (List[Union[int, float]]): The y coordinates of the stem chart.
        title (str, optional): The title of the chart. Default is an empty string.
        x_label (str, optional): The label for the x-axis. Default is an empty string.
        y_label (str, optional): The label for the y-axis. Default is an empty string.
        linefmt (str, optional): The format for the lines connecting the stems. Default is "C0-" (blue solid line).
        markerfmt (str, optional): The format for the markers at the top of the stems. Default is "C0o" (blue circle markers).
        basefmt (str, optional): The format for the baseline of the stems. Default is "k-" (black solid line).
        bottom (float, optional): The baseline position for the stems. Default is 0.
        orientation (str, optional): The orientation of the stems ("vertical" or "horizontal"). Default is "vertical".

    Returns:
        str: The URL link of the uploaded stem chart image on Imgur.

    Example:
        >>> draw_stem_chart([1, 2, 3], [2, 3, 4], title="Stem Plot", color="red")
        'https://imgur.com/your-uploaded-image-link'

    """
    chart = StemChart(title=title, x_label=x_label, y_label=y_label,
                      linefmt=linefmt, markerfmt=markerfmt, basefmt=basefmt,
                      bottom=bottom, orientation=orientation)
    fig = chart.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link

@mcp.tool()
def draw_step_chart(x_data: List[Union[str, int, float]], y_data: List[Union[int, float]],
                    title: str = "", x_label: str = "", y_label: str = "",
                    color: str = "blue", linestyle: str = "-", marker: str = "",
                    linewidth: float = 1.5, where: str = "pre") -> str:
    """
    Plots a step chart using the provided x and y data with optional customization 
    for the chart title, axis labels, line style, marker, line width, and step alignment, 
    and uploads the generated chart image to Imgur.

    Args:
        x_data (List[Union[str, int, float]]): The x coordinates for the step chart.
        y_data (List[Union[int, float]]): The y coordinates for the step chart.
        title (str, optional): The title of the chart. Default is an empty string.
        x_label (str, optional): The label for the x-axis. Default is an empty string.
        y_label (str, optional): The label for the y-axis. Default is an empty string.
        color (str, optional): The color of the step line. Default is "blue".
        linestyle (str, optional): The line style for the steps. Default is a solid line ("-").
        marker (str, optional): The marker for the step chart. Default is no marker ("").
        linewidth (float, optional): The width of the step line. Default is 1.5.
        where (str, optional): Defines the alignment of the steps. Options are "pre", "post", or "mid". Default is "pre".

    Returns:
        str: The URL link of the uploaded step chart image on Imgur.

    Example:
        >>> draw_step_chart([1, 2, 3], [2, 3, 4], title="Step Chart", color="red")
        'https://imgur.com/your-uploaded-image-link'

    """
    chart = StepChart(title=title, x_label=x_label, y_label=y_label, color=color,
                      linestyle=linestyle, marker=marker, linewidth=linewidth, where=where)
    fig = chart.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link


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
        A URL string linking to the generated violin plot chart image hosted online.
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

    image_bytes = buf.read()
    link = upload_image_to_imgur(client_id,image_host_url, image_bytes)

    return link


if __name__ == "__main__":
    # Register the service with the server
    mcp.run(transport="sse")