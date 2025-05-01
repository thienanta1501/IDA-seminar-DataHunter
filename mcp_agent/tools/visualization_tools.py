"""Visualization tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
visualization tools.
"""

from typing import Any, Dict, List, Optional, Union
#import aiohttp
from langchain.tools import BaseTool
from datetime import datetime
from mcp_agent.mcp_client import get_mcp_client

async def draw_bar_chart(x_data: List[Union[str, int, float]], y_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
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
    try:
        print("Da vao tool ve bar chart")
        mcp_client = await get_mcp_client()
        print("Lay duoc mcp client")
        params = {
            "x_data": x_data,
            "y_data": y_data,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "color": color,
            "type": type 
        }

        tool_name = "draw_bar_chart"

        result = await mcp_client.process_query(tool_name, params=params)
        print("Thuc hien xong ve chart")
        return result
    except Exception as e:
        print(f"Exception when call tool draw bar chart {e}")
        return f"Exception when call tool draw bar chart {e}"


async def draw_barh_chart(y_data: List[Union[str, int, float]], x_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
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
    try:
        mcp_client = await get_mcp_client()
        
        params = {
            "x_data": x_data,
            "y_data": y_data,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "color": color,
            "type": type
        }

        # Tên tool bạn định gọi
        tool_name = "draw_barh_chart"

        # Gọi xử lý thông qua MCP
        result = await mcp_client.process_query(tool_name, params=params)

        return result

    except Exception as e:
        print(f"Exception when calling tool draw_barh_chart: {e}")
        return f"Exception when calling tool draw_barh_chart: {e}"
    
async def draw_boxplot_chart(data: Dict[str, List[float]], title: str = "", x_label: str = "", y_label: str = "",
                       notch: bool = False, vert: bool = True, showmeans: bool = False,
                       showcaps: bool = True, showbox: bool = True, showfliers: bool = True,
                       widths: List[float] = None, positions: List[int] = None, 
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
    try:
        mcp_client = await get_mcp_client()
        tool_name = "draw_boxplot_chart"
        params = {
            "data": data,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "notch": notch,
            "vert": vert,
            "showmeans": showmeans,
            "showcaps": showcaps,
            "showbox": showbox,
            "showfliers": showfliers,
            "widths": widths,
            "positions": positions
        }

        result = await mcp_client.process_query(tool_name, params=params)
        print(f"type cua result la: {type(result)}")
        return result
    except Exception as e:
        print(f"Exception when calling tool draw_boxplot_chart: {e}")
        return f"Exception when calling tool draw_boxplot_chart: {e}"
    
async def draw_hist_chart(category: Optional[Dict[str, List[Union[int, float]]]] = None, 
                            data: Optional[List[Union[int, float]]] = None, 
                            bins: int = 10, title: str = "", 
                            x_label: str = "", y_label: str = "", 
                            color: Optional[Union[str, List[str]]] = None, 
                            alpha: float = 0.75, stacked: bool = False) -> str:
    """
    Generate a histogram (distribution chart) from the given data and return it as an url string of image.

    Parameters:
        category (dict): A dictionary where keys are categories and values are lists of numeric values for each group.
        data (list): A list of numeric values for a single dataset (if category is not provided).
        bins (int): The number of histogram bins (default is 10).
        title (str): The title of the chart. Always name this field if data is not none
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        color (Optional[str or list]): The color of the bars (default is None). Can be a single color or a list of colors.
        alpha (float): The transparency of the bars (default is 0.75).
        stacked (bool): Whether the bars should be stacked (default is False).

    Returns:
        A URL string linking to the generated distribution chart image hosted online.
    """

    try:
        mcp_client = await get_mcp_client()

        tool_name = "draw_hist_chart"
        params = {
            "category": category,
            "data": data,
            "bins": bins,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "color": color,
            "alpha": alpha,
            "stacked": stacked
        }

        result = await mcp_client.process_query(tool_name, params=params)

        return result
    except Exception as e:
        print(f"Exception when call tool draw hist chart {e}")
        return f"Exception when call tool draw hist chart {e}"
    
async def draw_line_chart(x_data: List[Union[str, int, float]] , y_data: Dict[Union[str], List[Union[float, int]]], title: str = "", x_label: str = "", y_label: str = "",
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
    try:
        mcp_client = await get_mcp_client()
        tool_name = "draw_line_chart"
        params = {
            "x_data": x_data,
            "y_data": y_data,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "linestyle": linestyle,
            "linewidth": linewidth,
            "marker": marker,
            "color": color,
            "scalex": scalex,
            "scaley": scaley
        }

        result = await mcp_client.process_query(tool_name, params=params)
        return result
    except Exception as e:
        print(f"Exception when call tool draw line chart {e}")
        return f"Exception when call tool draw line chart {e}"
    
async def draw_pie_chart(x: List[Union[int, float]], labels: Optional[List[str]] = None, explode: Optional[List[float]] = None,
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
    try:
        mcp_client = await get_mcp_client()
        tool_name = "draw_pie_chart"
        params = {
            "x": x,
            "labels": labels,
            "explode": explode,
            "colors": colors,
            "autopct": autopct,
            "pctdistance": pctdistance,
            "shadow": shadow,
            "labeldistance": labeldistance,
            "startangle": startangle,
            "radius": radius,
            "counterclock": counterclock,
            "center": center,
            "frame": frame,
            "rotatelabels": rotatelabels,
            "normalize": normalize,
            "title": title
        }

        result = await mcp_client.process_query(tool_name, params=params)

        return result
    except Exception as e:
        print(f"Exception when call tool draw pie chart {e}")
        return f"Exception when call tool draw pie chart {e}"
    
async def draw_scatter_chart(
    x: List[float],
    y: List[float],
    s: Union[float, List[float]] = 20.0,  # Kích thước điểm, có thể là scalar hoặc array
    c: Union[float, str, List[Union[float, str]]]=[],  # Màu sắc điểm, có thể là scalar, string hoặc list
    marker: str = 'o',
    cmap: str = "",
    vmin: float = 0.0,
    vmax: float = 1.0,
    alpha: float = 1.0,
    linewidths: float = 0.5,
    edgecolors: str = 'face',
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
        vmin (float, optional): Minimum value for colormap normalization.
        vmax (float, optional): Maximum value for colormap normalization.
        alpha (float, optional): Opacity level of points (0 to 1).
        linewidths (float, optional): Width of point edges.
        edgecolors (str, optional): Edge color for points.
        plotnonfinite (bool): Whether to plot NaN/inf points (default: False).
        title (str): Title of the chart.

    Returns:
        A URL string linking to the generated scatter chart image hosted online.
    """
    try:
        mcp_client = await get_mcp_client()
        tool_name = "draw_scatter_chart"
        params = {
            "x": x,
            "y": y,
            "s": s,
            "c": c,
            "marker": marker,
            "cmap": cmap,
            "vmin": vmin,
            "vmax": vmax,
            "alpha": alpha,
            "linewidths": linewidths,
            "edgecolors": edgecolors,
            "plotnonfinite": plotnonfinite,
            "title": title
        }

        result = await mcp_client.process_query(tool_name, params=params)

        return result
    except Exception as e:
        print(f"Exception when call tool draw scatter chart {e}")
        return f"Exception when call tool draw scatter chart {e}"
    
async def draw_pearson_correlation_chart(data: Dict[str, List[Union[int, float, str, datetime]]], title: str) -> str:
    """
    Generates a Pearson correlation chart from the provided data and uploads the chart image to a hosting server.

    Args:
        data (Dict[str, List[Union[int, float, str, datetime]]]): 
            A dictionary where each key is a column name and each value is a list of values.
            The values can be integers, floats, strings, or datetime objects.
        title (str): 
            The title to be displayed on the chart.

    Returns:
        str: 
            A URL linking to the uploaded image of the generated correlation chart.

    Notes:
        - If non-numeric values (e.g., strings or datetimes) are provided, they should be preprocessed or encoded appropriately
          inside the PearsonCorrelation.create_chart method, as Pearson correlation requires numerical inputs.
    """

    try:
        mcp_client = await get_mcp_client()
        tool_name = "draw_pearson_correlation_chart"
        params = {
            "data": data,
            "title": title
        }
        result = await mcp_client.process_query(tool_name, params=params)

        return result
    except Exception as e:
        print(f"Exception when call tool draw pearson correlation chart {e}")
        return f"Exception when call tool draw pearson correlation chart {e}"