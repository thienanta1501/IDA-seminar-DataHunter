"""Visualization tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
visualization tools.
"""

from typing import Any, Dict, List, Optional, Union

#import aiohttp
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class VisualizationInput(BaseModel):
    """Input for the visualization tool."""
    
    chart_type: str = Field(
        ...,
        description="Type of chart to generate (bar, line, scatter, pie, etc.)",
    )
    data: Union[Dict[str, Any], str] = Field(
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


class VisualizationTool(BaseTool):
    """Tool for generating visualizations."""
    
    name = "visualize_tool"
    description = "Generates visualizations using Matplotlib based on input parameters (chart type, data, etc.) and returns a .jpg or .png image."
    args_schema = VisualizationInput
    
    def __init__(self, server_url: str):
        """Initialize the tool.
        
        Args:
            server_url: URL of the MCP server.
        """
        super().__init__()
        self.server_url = server_url
    
    async def _arun(
        self,
        chart_type: str,
        data: Union[Dict[str, Any], str],
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        color: Optional[str] = None,
        figsize: Optional[tuple[int, int]] = None,
        **kwargs: Any,
    ) -> str:
        """Run the tool asynchronously.
        
        Args:
            chart_type: Type of chart to generate.
            data: Data to visualize.
            x_column: Column to use for the x-axis.
            y_column: Column to use for the y-axis.
            title: Title for the chart.
            x_label: Label for the x-axis.
            y_label: Label for the y-axis.
            color: Color for the chart.
            figsize: Figure size.
            **kwargs: Additional tool arguments.
            
        Returns:
            The visualization as a base64-encoded image.
        """
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(
        #         f"{self.server_url}/tools/visualize_tool",
        #         json={
        #             "chart_type": chart_type,
        #             "data": data,
        #             "x_column": x_column,
        #             "y_column": y_column,
        #             "title": title,
        #             "x_label": x_label,
        #             "y_label": y_label,
        #             "color": color,
        #             "figsize": figsize,
        #         },
        #     ) as response:
        #         result = await response.json()
        #         return result["image"]
        return "Mock"
    
    def _run(
        self,
        chart_type: str,
        data: Union[Dict[str, Any], str],
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        color: Optional[str] = None,
        figsize: Optional[tuple[int, int]] = None,
        **kwargs: Any,
    ) -> str:
        """Run the tool synchronously.
        
        Args:
            chart_type: Type of chart to generate.
            data: Data to visualize.
            x_column: Column to use for the x-axis.
            y_column: Column to use for the y-axis.
            title: Title for the chart.
            x_label: Label for the x-axis.
            y_label: Label for the y-axis.
            color: Color for the chart.
            figsize: Figure size.
            **kwargs: Additional tool arguments.
            
        Returns:
            The visualization as a base64-encoded image.
        """
        raise NotImplementedError("This tool only supports async execution") 