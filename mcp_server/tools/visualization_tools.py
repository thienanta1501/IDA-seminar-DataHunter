"""Visualization tools for the MCP Server.

This module provides tools for generating visualizations using Matplotlib.
"""

import base64
import io
from typing import Any, Dict, List, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
from mcp.server.fastmcp import Context
from mcp.server.fastmcp.utilities.types import Image
from pydantic import BaseModel, Field
from ..utils.index import post_image_to_host_server
from mcp_server.tools.charts.barchart import BarChart
from mcp_server.tools.charts.barhchart import BarhChart
from mcp_server.tools.charts.boxplotchart import BoxPlotChart
from mcp_server.tools.charts.histchart import HistChart
from mcp_server.tools.charts.linechart import LineChart
from mcp_server.tools.charts.piechart import PieChart


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