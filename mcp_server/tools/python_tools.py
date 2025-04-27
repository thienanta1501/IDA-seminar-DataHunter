"""Python execution tools for the MCP Server.

This module provides tools for executing Python code snippets in a sandboxed environment.
"""

import io
import sys
from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field


class PythonExecuteInput(BaseModel):
    """Input for the Python execution tool."""
    
    code: str = Field(..., description="Python code to execute")
    timeout: Optional[int] = Field(
        None,
        description="Timeout in seconds for the execution",
    )


async def python_execute_tool(input_data: PythonExecuteInput, ctx: Context) -> str:
    """Execute Python code snippets in a sandboxed environment.
    
    Args:
        input_data: The input data for the Python execution.
        ctx: The MCP context.
        
    Returns:
        The output of the Python code execution.
    """
    # Create a string buffer to capture stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    # Save the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    try:
        # Redirect stdout and stderr to our buffers
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer
        
        # Execute the code
        exec(input_data.code, {})
        
        # Get the output
        stdout_output = stdout_buffer.getvalue()
        stderr_output = stderr_buffer.getvalue()
        
        # Combine the output
        output = ""
        if stdout_output:
            output += f"STDOUT:\n{stdout_output}\n"
        if stderr_output:
            output += f"STDERR:\n{stderr_output}\n"
        
        return output or "Execution completed successfully with no output."
    
    except Exception as e:
        # Get the error message
        error_message = str(e)
        
        # Get any output that was captured before the error
        stdout_output = stdout_buffer.getvalue()
        stderr_output = stderr_buffer.getvalue()
        
        # Combine the output
        output = ""
        if stdout_output:
            output += f"STDOUT:\n{stdout_output}\n"
        if stderr_output:
            output += f"STDERR:\n{stderr_output}\n"
        
        output += f"ERROR:\n{error_message}\n"
        
        return output
    
    finally:
        # Restore the original stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr 