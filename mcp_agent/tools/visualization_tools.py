"""Visualization tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
visualization tools.
"""

from typing import Any, Dict, List, Optional, Union
#import aiohttp
from langchain.tools import BaseTool
from datetime import datetime
import pandas as pd
from mcp_agent.mcp_client import get_mcp_client
    
async def draw_bar_chart(file_path: str, x_column: str, y_column: List[str], title: str, x_label: str, y_label: str, color: str = "skyblue", type: str = "simple"):
    """
    draw a bar chart using data from a CSV file that contains data. Use this tool when query result has been saved before

    This function reads data from the given CSV file, extracts the specified columns,
    and sends a request to the server to generate a bar chart. The chart type can be 
    one of "simple", "grouped", or "stacked".

    Args:
        file_path (str): The path to the CSV file containing the data. Extract file path in list message.
        x_column (str): The name of the column to be used for the x-axis.
        y_column (List[str]): A list of column names to be used for the y-axis.
        title (str): The title of the chart.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        color (str, optional): The color to use for the bars. Defaults to "skyblue".
        type (str, optional): The type of bar chart to generate. 
            Options are "simple", "grouped", or "stacked". Defaults to "simple".

    Returns:
        Any: The result returned from the server after processing the chart request.

    Raises:
        Exception: If an error occurs during the process, an exception message will be returned.
    """
    
    try:
        mcp_client = await get_mcp_client()
        df = pd.read_csv(file_path)
        tool_name = "draw_bar_chart"
        x_data = df[x_column].to_list()
        y_data = {}

        for column in y_column:
            y_data[column] = df[column].to_list()
        
        params = {
            "x_data": x_data,
            "y_data": y_data,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "color": color,
            "type": type 
        }

        result = await mcp_client.process_query(tool_name, params=params)
        print("Thuc hien xong ve chart")
        return result
    except Exception as e:
        print(f"Exception when call tool draw bar chart {e}")
        return f"Exception when call tool draw bar chart {e}"
    
async def draw_barh_chart(file_path: str, y_column: str, x_columns: List[str], \
                               title: str, x_label: str, y_label: str, color: str = "skyblue", type: str = "simple"):
    """
    draws a horizontal bar chart based on data from a CSV file 

    Args:
        file_path (str): Path to the CSV file containing the data.
        y_column (str): Name of the column to be used for y-axis labels.
        x_columns (List[str]): List of column names to be used for x-axis values.
        title (str): Title of the chart.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        color (str, optional): Color of the bars. Defaults to "skyblue".
        type (str, optional): Type of the bar chart (must be one of "simple", "stacked" or "grouped"). Defaults to "simple".

    Returns:
        str: a string represent image link.

    Raises:
        Exception: If any error occurs during processing, it will be caught and logged.
    """
    try:
        mcp_client = await get_mcp_client()
        df = pd.read_csv(file_path)
        y_data = df[y_column].to_list()
        x_data = {}

        for column in x_columns:
            x_data[column] = df[column].to_list()

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
    
async def draw_boxplot_chart(file_path: str, column_data: List[str], title: str = "", x_label: str = "", y_label: str = "",
                       notch: bool = False, vert: bool = True, showmeans: bool = False,
                       showcaps: bool = True, showbox: bool = True, showfliers: bool = True,
                       widths: List[float] = None, positions: List[int] = None, 
                       ) -> str:
    """
    Generate a boxplot chart from the given data and return it as an image link.

    Parameters:
        file_path (str): Path to the CSV file containing the data.
        column_data (List[str]): list of names of the columns to be used to extract data.
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
        df = pd.read_csv(file_path)
        data = {}

        for column in column_data:
            data[column] = df[column].to_list()

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
    
async def draw_hist_chart(file_path: str, columns: List[str],bins: int = 10, title: str = "", 
                            x_label: str = "", y_label: str = "", 
                            color: Optional[Union[str, List[str]]] = None, 
                            alpha: float = 0.75, stacked: bool = False) -> str:
    """
    Generate a histogram (distribution chart) from the given data and return it as an url string of image.

    Parameters:
        file_path (str): Path to the CSV file containing the data.
        columns (List[str]): list of names of the columns to be used to extract data.
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
        df = pd.read_csv(file_path)
        category = None
        data = None

        if len(columns) == 1:
            data = df[columns[0]].to_list()
        elif len(columns) > 1:
            category = {}

            for column in columns:
                category[column] = df[column].to_list()

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
    
async def draw_line_chart(file_path: str, x_column: str, y_column: str, label_column: str = "", title: str = "", x_label: str = "", y_label: str = "",
                    linestyle: str = "-", linewidth: float = 2, marker: Optional[str] = None,
                    color: Optional[str] = None, scalex: bool = True, scaley: bool = True) -> str:
    """
    Draws a multi-line chart using the given x-axis values and multiple y-axis data series,
    and returns the chart image as a PNG binary string.

    Args:
        file_path (str): Path to the CSV file containing the data.
        x_column (str): The name of the column to be used for the x-axis.
        y_column (str): A column name to be used for the y-axis.
        label_column(str): A column name to set label for line chart. Default to "".
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
        df = pd.read_csv(file_path)
        x_data = df[x_column].unique().tolist()
        print(x_data)
        if label_column != "":
            labels = df[label_column].unique().tolist()
        else:
            labels = []
        
        y_data= {}

        for label in labels:
            y_data[label] = [0 for i in range(len(x_data))]

        index_map = {}

        for i in range(len(x_data)):
            index_map[x_data[i]] = i

        for label in labels:
            label_df = df[df[label_column] == label]

            for index, row in label_df.iterrows():
                y_data[label][index_map[row[x_column]]] = row[y_column]
        
        if len(labels) == 0:
            y_data["value"] = df[y_column].tolist()

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
        print("Call line chart agent")
        result = await mcp_client.process_query(tool_name, params=params)
        return result
    except Exception as e:
        print(f"Exception when call tool draw line chart {e}")
        return f"Exception when call tool draw line chart {e}"
    
async def draw_pie_chart(file_path: str, column: str, labels: Optional[List[str]] = None, explode: Optional[List[float]] = None,
                   colors: Optional[List[str]] = None, autopct: Optional[str] = None, pctdistance: float = 0.6, 
                   shadow: bool = False, labeldistance: float = 1.1, startangle: float = 0, radius: float = 1, 
                   counterclock: bool = True, center: List[float] = [0, 0], frame: bool = False, 
                   rotatelabels: bool = False, normalize: bool = True, title: str = "") -> str:
    """
    Generate a pie chart from the given data and return it as an image url.

    Parameters:
        file_path (str): Path to the CSV file containing the data.
        column (str): column that contains data to draw chart.
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
        df = pd.read_csv(file_path)
        x = df[column].to_list()

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
    file_path: str,
    x_column: str,
    y_column: str,
    s_column: str = "",  # Kích thước điểm, có thể là scalar hoặc array
    c_column: str = "",  # Màu sắc điểm, có thể là scalar, string hoặc list
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
    Asynchronously draws a scatter chart based on data from a CSV file using the MCP client.

    Args:
        file_path (str): Path to the CSV file containing the data.
        x_column (str): Name of the column to use for x-axis values.
        y_column (str): Name of the column to use for y-axis values.
        s_column (str, optional): Name of the column specifying point sizes. If empty, a default size is used. Defaults to "".
        c_column (str, optional): Name of the column specifying point colors. If empty, a default color is used. Defaults to "".
        marker (str, optional): Marker style for the scatter points. Defaults to 'o'.
        cmap (str, optional): Colormap name for coloring the points. Defaults to "".
        vmin (float, optional): Minimum data value that corresponds to the colormap. Defaults to 0.0.
        vmax (float, optional): Maximum data value that corresponds to the colormap. Defaults to 1.0.
        alpha (float, optional): Transparency level of the points. Defaults to 1.0.
        linewidths (float, optional): Width of the marker edges. Defaults to 0.5.
        edgecolors (str, optional): Color of the marker edges. Defaults to 'face'.
        plotnonfinite (bool, optional): Whether to plot points with nonfinite (NaN or Inf) values. Defaults to False.
        title (str, optional): Title of the scatter plot. Defaults to "".

    Returns:
        str: The URL of the generated scatter chart image.

    Raises:
        Exception: If any error occurs during the process, it is caught and logged.
    """
    try:
        mcp_client = await get_mcp_client()
        df = pd.read_csv(file_path)
        x = df[x_column].to_list()
        y = df[y_column].to_list()
        s, c = 20.0, []
        if s_column:
            s = df[s_column].to_list()
        if c_column:
            c = df[c_column].to_list()

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

        image_url = await mcp_client.process_query(tool_name, params=params)

        return image_url
    except Exception as e:
        print(f"Exception when call tool draw scatter chart {e}")
        return f"Exception when call tool draw scatter chart {e}"

async def draw_pearson_correlation_chart(file_path: str, columns: List[str], title: str) -> str:
    """
    Asynchronously generates a Pearson correlation chart from specified columns in a CSV file 
    and uploads the resulting chart image to a hosting server.

    Args:
        file_path (str): 
            Path to the CSV file containing the dataset.
        columns (List[str]): 
            List of column names to include in the correlation analysis.
        title (str): 
            Title to be displayed on the correlation chart.

    Returns:
        str: 
            A URL linking to the uploaded image of the generated correlation chart.

    Raises:
        Exception: 
            Any errors during processing will be caught and logged.

    Notes:
        - Input columns must contain numerical data, as Pearson correlation requires numeric inputs.
        - Any non-numeric columns (e.g., strings, datetimes) should be preprocessed before using this function.
    """

    try:
        mcp_client = await get_mcp_client()
        df = pd.read_csv(file_path)
        data = {}

        for column in columns:
            data[column] = df[column].to_list()
        
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