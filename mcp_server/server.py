"""MCP Server for AI-Driven Data Application.

This module provides the DataServer class, which implements the MCP server
for the AI-Driven Data Application. The server provides tools for data querying,
visualization, machine learning, and Python code execution.
"""

import os
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from mcp_server.tools.db_tools import get_db_structure, sql_tool
from mcp_server.tools.ml_tools import build_ml_model
from mcp_server.tools.python_tools import python_execute_tool
from mcp_server.tools.stats_tools import generate_html_report
from mcp_server.tools.visualization_tools import draw_bar_chart, draw_barh_chart, draw_boxplot_chart, \
draw_hist_chart, draw_line_chart, draw_pie_chart, draw_scatter_chart, draw_pearson_correlation_chart


class DataServer:
    """MCP Server for AI-Driven Data Application.
    
    This server provides tools for data querying, visualization, machine learning,
    and Python code execution.
    """

    def __init__(
        self,
        name: str = "DataServer",
        instructions: Optional[str] = None,
        **settings: Any
    ):
        """Initialize the DataServer.
        
        Args:
            db_config: Database configuration. If None, will try to load from environment.
            name: Name of the server.
            instructions: Instructions for the server.
            **settings: Additional settings for the FastMCP server.
        """
        self.server = FastMCP(name=name, instructions=instructions, **settings)
       
        # Register tools
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register tools with the server."""
        # Database tools
        self.server.add_tool(
            get_db_structure,
            name="get_db_structure",
        )
        
        self.server.add_tool(
            sql_tool,
            name="sql_tool"
        )

        # Visualization tools

        self.server.add_tool(
            draw_bar_chart,
            name="draw_bar_chart"
        )

        self.server.add_tool(
            draw_barh_chart,
            name="draw_barh_chart"
        )

        self.server.add_tool(
            draw_boxplot_chart,
            name="draw_boxplot_chart"
        )
        
        self.server.add_tool(
            draw_hist_chart,
            name = "draw_hist_chart"
        )

        self.server.add_tool(
            draw_line_chart,
            name="draw_line_chart"
        )

        self.server.add_tool(
            draw_pie_chart,
            name="draw_pie_chart"
        )

        self.server.add_tool(
            draw_scatter_chart,
            name="draw_scatter_chart"
        )

        self.server.add_tool(
            draw_pearson_correlation_chart,
            name="draw_pearson_correlation_chart"
        )

        # Python execution tool
        self.server.add_tool(
            python_execute_tool,
            name="python_execute_tool",
        )
        
        # Machine learning tool
        self.server.add_tool(
            build_ml_model,
            name="build_ml_model",
        )

        # Statistic tool
        self.server.add_tool(
            generate_html_report,
            name="generate_html_report"
        )


    def run(self, transport: str = "stdio") -> None:
        """Run the server.
        
        Args:
            transport: Transport protocol to use ("stdio" or "sse").
        """
        self.server.run(transport=transport) 


# server = FastMCP(name="DataServer", instructions="I am a data server that provides tools for data querying, visualization, machine learning, and Python code execution.")

# server.add_tool(get_db_structure, name="get_db_structure")

# server.add_tool(sql_tool, name="sql_tool")

# server.run(transport="stdio")