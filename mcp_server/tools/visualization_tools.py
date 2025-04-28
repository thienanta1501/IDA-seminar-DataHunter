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
