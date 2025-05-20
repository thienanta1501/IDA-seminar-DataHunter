"""Visualization tools for the MCP Server.

This module provides tools for generating visualizations using Matplotlib.
"""

import base64
from csv import Error
import io
from typing import Any, Dict, List, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
from mcp.server.fastmcp import Context
from mcp.server.fastmcp.utilities.types import Image
from pydantic import BaseModel, Field
from datetime import datetime
from ..utils.index import post_image_to_host_server
from mcp_server.tools.charts.barchart import BarChart
from mcp_server.tools.charts.barhchart import BarhChart
from mcp_server.tools.charts.boxplotchart import BoxPlotChart
from mcp_server.tools.charts.histchart import HistChart
from mcp_server.tools.charts.linechart import LineChart
from mcp_server.tools.charts.piechart import PieChart
from mcp_server.tools.charts.scatterchart import ScatterChart
from mcp_server.tools.charts.pearson_correlation import PearsonCorrelation


def draw_bar_chart(x_data: List[Union[str, int, float]], y_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
                   type: str = "simple") -> str:

    bar_chart_object = BarChart(title = title, x_label = x_label, y_label = y_label, color = color, type = type)
    fig = bar_chart_object.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = post_image_to_host_server(image_bytes)

    return link

def draw_barh_chart(y_data: List[Union[str, int, float]], x_data: dict[str, list], title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue",
                   type: str = "simple") -> str:

    bar_chart_object = BarhChart(title = title, x_label = x_label, y_label = y_label, color = color, type = type)
    fig = bar_chart_object.create_chart(y_data_labels=y_data, x_data_dict=x_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    link = post_image_to_host_server(image_bytes)

    return link

def draw_boxplot_chart(data: Dict[str, List[float]], title: str = "", x_label: str = "", y_label: str = "",
                       notch: bool = False, vert: bool = True, showmeans: bool = False,
                       showcaps: bool = True, showbox: bool = True, showfliers: bool = True,
                       widths: Optional[List[float]] = None, positions: Optional[List[int]] = None, 
                       ) -> str:
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
    link = post_image_to_host_server(image_bytes)

    return link

def draw_hist_chart(category: Optional[Dict[str, List[Union[int, float]]]] = None, 
                            data: Optional[List[Union[int, float]]] = None, 
                            bins: int = 10, title: str = "", 
                            x_label: str = "", y_label: str = "", 
                            color: Optional[Union[str, List[str]]] = None, 
                            alpha: float = 0.75, stacked: bool = False) -> str:
    if category:
        chart = HistChart(
            title=title, x_label=x_label, y_label=y_label, color=color, bins=bins,
            alpha=alpha, category=category, stacked=stacked
        )
    elif data:
        chart = HistChart(
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
    link = post_image_to_host_server(image_bytes)

    return link

def draw_line_chart(x_data: List[Union[str, int, float]] , y_data: Dict[Union[str], List[Union[float, int]]], title: str = "", x_label: str = "", y_label: str = "",
                    linestyle: str = "-", linewidth: float = 2, marker: Optional[str] = None,
                    color: Optional[str] = None, scalex: bool = True, scaley: bool = True) -> str:
    try:
        chart = LineChart(
            title=title, x_label=x_label, y_label=y_label,
            linestyle=linestyle, linewidth=linewidth, marker=marker,
            color=color, scalex=scalex, scaley=scaley
        )
        print("Vao create chart")
        fig = chart.create_chart(x_data=x_data, y_data=y_data)
    except Exception as e:
        raise Exception(f"{e}")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_bytes = buf.read()
    link = post_image_to_host_server(image_bytes)

    return link

def draw_pie_chart(x: List[Union[int, float]], labels: Optional[List[str]] = None, explode: Optional[List[float]] = None,
                   colors: Optional[List[str]] = None, autopct: Optional[str] = None, pctdistance: float = 0.6, 
                   shadow: bool = False, labeldistance: float = 1.1, startangle: float = 0, radius: float = 1, 
                   counterclock: bool = True, center: List[float] = [0, 0], frame: bool = False, 
                   rotatelabels: bool = False, normalize: bool = True, title: str = "") -> str:
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
    link = post_image_to_host_server(image_bytes)

    return link

def draw_scatter_chart(
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
        vmin=vmin,
        vmax=vmax,
        alpha=alpha,
        linewidths=linewidths,
        edgecolors=edgecolors,
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
    link = post_image_to_host_server(image_bytes)

    return link

def draw_pearson_correlation_chart(data: Dict[str, List[Union[int, float, str, datetime]]], title: str) -> str:
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
    chart_object = PearsonCorrelation(title=title)
    fig = chart_object.create_chart(data)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_bytes = buf.read()
    link = post_image_to_host_server(image_bytes)
    return link
