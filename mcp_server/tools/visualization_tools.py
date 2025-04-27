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


class VisualizationInput(BaseModel):
    """Input for the visualization tool."""
    
    chart_type: str = Field(
        ...,
        description="Type of chart to generate (bar, line, scatter, pie, etc.)",
    )
    data: Union[str] = Field(
        ...,
        description="Data to visualize, either as a DataFrame or a CSV string",
    )
    x_column: Optional[str] = Field(
        None,
        description="Column to use for the x-axis",
    )
    y_column: Optional[str] = Field(
        None,
        description="Column to use for the y-axis",
    )
    title: Optional[str] = Field(
        None,
        description="Title for the chart",
    )
    x_label: Optional[str] = Field(
        None,
        description="Label for the x-axis",
    )
    y_label: Optional[str] = Field(
        None,
        description="Label for the y-axis",
    )
    color: Optional[str] = Field(
        None,
        description="Color for the chart",
    )
    figsize: Optional[tuple[int, int]] = Field(
        None,
        description="Figure size as a tuple of (width, height)",
    )


async def visualize_tool(input_data: VisualizationInput, ctx: Context) -> Image:
    """Generate a visualization using Matplotlib.
    
    Args:
        input_data: The input data for the visualization.
        ctx: The MCP context.
        
    Returns:
        The visualization as an Image.
    """
    # Parse the data if it's a string
    if isinstance(input_data.data, str):
        df = pd.read_csv(io.StringIO(input_data.data))
    else:
        df = input_data.data
    
    # Create the figure
    plt.figure(figsize=input_data.figsize or (10, 6))
    
    # Generate the chart based on the chart type
    if input_data.chart_type.lower() == "bar":
        if input_data.x_column and input_data.y_column:
            plt.bar(
                df[input_data.x_column],
                df[input_data.y_column],
                color=input_data.color,
            )
        else:
            # If no columns specified, use the first two columns
            columns = df.columns.tolist()
            if len(columns) >= 2:
                plt.bar(
                    df[columns[0]],
                    df[columns[1]],
                    color=input_data.color,
                )
            else:
                raise ValueError("Not enough columns in the data for a bar chart")
    
    elif input_data.chart_type.lower() == "line":
        if input_data.x_column and input_data.y_column:
            plt.plot(
                df[input_data.x_column],
                df[input_data.y_column],
                color=input_data.color,
            )
        else:
            # If no columns specified, use the first two columns
            columns = df.columns.tolist()
            if len(columns) >= 2:
                plt.plot(
                    df[columns[0]],
                    df[columns[1]],
                    color=input_data.color,
                )
            else:
                raise ValueError("Not enough columns in the data for a line chart")
    
    elif input_data.chart_type.lower() == "scatter":
        if input_data.x_column and input_data.y_column:
            plt.scatter(
                df[input_data.x_column],
                df[input_data.y_column],
                color=input_data.color,
            )
        else:
            # If no columns specified, use the first two columns
            columns = df.columns.tolist()
            if len(columns) >= 2:
                plt.scatter(
                    df[columns[0]],
                    df[columns[1]],
                    color=input_data.color,
                )
            else:
                raise ValueError("Not enough columns in the data for a scatter chart")
    
    elif input_data.chart_type.lower() == "pie":
        if input_data.y_column:
            plt.pie(
                df[input_data.y_column],
                labels=df[input_data.x_column] if input_data.x_column else None,
                autopct="%1.1f%%",
            )
        else:
            # If no columns specified, use the first two columns
            columns = df.columns.tolist()
            if len(columns) >= 2:
                plt.pie(
                    df[columns[1]],
                    labels=df[columns[0]],
                    autopct="%1.1f%%",
                )
            else:
                raise ValueError("Not enough columns in the data for a pie chart")
    
    else:
        raise ValueError(f"Unsupported chart type: {input_data.chart_type}")
    
    # Set the title and labels
    if input_data.title:
        plt.title(input_data.title)
    
    if input_data.x_label:
        plt.xlabel(input_data.x_label)
    
    if input_data.y_label:
        plt.ylabel(input_data.y_label)
    
    # Save the figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    
    # Convert to base64
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    
    # Close the figure to free memory
    plt.close()
    
    # Return as an Image
    return Image.from_base64(img_str) 