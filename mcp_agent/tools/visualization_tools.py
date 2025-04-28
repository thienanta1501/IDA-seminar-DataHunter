"""Visualization tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
visualization tools.
"""

from typing import Any, Dict, List, Optional, Union
#import aiohttp
from langchain.tools import BaseTool
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

        tool_name = "draw_bar_chart"

        result = await mcp_client.process_query(tool_name, params=params)

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