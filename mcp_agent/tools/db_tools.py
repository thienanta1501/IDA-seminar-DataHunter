"""Database tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
database tools.
"""

import json
from typing import Any, Dict, List, Optional, Union

#import aiohttp
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from mcp_agent.mcp_client import get_mcp_client
# --- Converted Function: get_db_structure ---
async def get_db_structure() -> str:
    """
    Retrieves the PostgreSQL database schema via the MCP client and returns it as a string.
    This is used to understand the available tables and columns for query generation.
    """
    print("--- Tool: get_db_structure executing (real logic) ---")
    try:
        # Get the configured MCP client instance
        mcp_client = await get_mcp_client()
        params = {"schema_name": "public"}
        # Call the client method designated for retrieving the schema
        result = await mcp_client.process_query("get_db_structure", params)
        print(f"--- Tool: get_db_structure result received (length: {len(result) if isinstance(result, str) else 'N/A'}) ---")

        # Ensure the result is a string, as expected by LangChain tools
        if not isinstance(result, str):
            result = str(result) # Basic conversion if not already string

        return result

    except Exception as e:
        print(f"Error in get_db_structure tool: {type(e).__name__} - {e}")
        # Return an informative error message string
        return f"Error retrieving database structure: {type(e).__name__} - {e}"


# --- Converted Function: sql_tool ---
async def sql_tool(query: str, return_format: str = "dataframe") -> str:
    """
    Executes the given SQL query via the MCP client and handles the response
    returned by the client, ensuring the final output is a string suitable for LangChain.

    Args:
        query (str): The SQL query to execute. Should be syntactically correct SQL.
        return_format (str): The desired format requested from the server ('dataframe' or 'csv').
                             The MCP client/server interaction determines the actual format received.

    Returns:
        str: The query results as a string (e.g., CSV, JSON string representation of data,
             status message, or error message).
    """
    print(f"--- Client Tool: sql_tool preparing call via mcp_client ---")
    print(f"   Query: {query}")
    print(f"   Return Format Request: {return_format}")

    try:
        # Get the MCP client instance (handles actual network request)
        mcp_client = await get_mcp_client()
        # Prepare parameters for the client request
        params = {"query": query, "return_format": return_format}

        # --- Call the MCP client ---
        # 'result' contains whatever the MCP client layer returns after
        # communicating with the server and processing its response.
        result: Any = await mcp_client.process_query("sql_tool", params=params)

        print(f"--- Client Tool: sql_tool received result from mcp_client ---")
        print(f"   Result type: {type(result)}")
        # Log snippet for debugging, handle non-string types gracefully
        if isinstance(result, str):
             print(f"   Result snippet (str): {result[:500]}{'...' if len(result) > 250 else ''}")
        elif isinstance(result, (list, dict)):
             # Convert complex types to string for logging snippet
             result_str_snippet = str(result)
             print(f"   Result snippet (list/dict): {result_str_snippet[:500]}{'...' if len(result_str_snippet) > 250 else ''}")
        else:
             print(f"   Result (other type): {result}")

        final_output_str: str

        if isinstance(result, str):

            final_output_str = result
        elif isinstance(result, (dict, list)):

            try:
                final_output_str = json.dumps(result)

            except TypeError as json_err:
                print(f"Warning: Could not serialize mcp_client result ({type(result).__name__}) to JSON: {json_err}. Falling back to str().")
                final_output_str = str(result) # Fallback to generic string representation
        elif result is None:
            print("Warning: mcp_client returned None for sql_tool.")
            final_output_str = "Executed successfully, but no data was returned."
            if not query.strip().upper().startswith('SELECT'):
                final_output_str = "Command executed successfully."

        else:
            # Handle any other unexpected types returned by the client
            print(f"Warning: mcp_client returned unexpected type: {type(result).__name__}. Converting to string.")
            final_output_str = str(result)

        print(f"--- Client Tool: sql_tool returning final string (length: {len(final_output_str)}) ---")
        return final_output_str

    except Exception as e:
        # Catch errors occurring during the mcp_client call itself
        print(f"Error during mcp_client interaction for sql_tool: {type(e).__name__} - {e}")
        # Return an informative error message string back to the agent/LLM
        return f"Error executing SQL query '{query}' via MCP client: {type(e).__name__} - {e}"
