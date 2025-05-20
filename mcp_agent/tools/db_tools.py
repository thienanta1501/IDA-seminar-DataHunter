"""Database tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
database tools.
"""
SAVE_PATH_FILE = r"C:\Users\Admin\OneDrive - VNU-HCMUS\WORKSPACE\US\2024-2025_3-Junior\Semester-2\IDA\IDA-seminar-DataHunter\report_analysis"


import json
from typing import Any, Dict, List, Optional, Union
import pandas as pd
import random
import string
import asyncio
import json
import os
#import aiohttp
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import re
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


def handle_json(dirty_json: str):
    dirty_str = re.sub(r"Timestamp\('([\d\-:\s]+)'\)", r'"\1"', dirty_json)
    dirty_str = dirty_str.replace('NaT', 'null')
    dirty_str = dirty_str.replace("'", '"')
    return dirty_str


# --- Converted Function: sql_tool ---
async def sql_tool(query: str) -> str:
    """
    Executes the given SQL query via the MCP client and handles the response
    returned by the client, ensuring the final output is a string suitable for LangChain.

    Args:
        query (str): The SQL query to execute. Should be syntactically correct SQL.

    Returns:
        str: The query results as a string (e.g., CSV, JSON string representation of data,
             status message, error message, or a snippet with file save confirmation).
    """
    print(f"--- Client Tool: sql_tool preparing call via mcp_client ---")
    print(f"   Query: {query}")

    try:
        # Get the MCP client instance (handles actual network request)
        mcp_client = await get_mcp_client()
        # Prepare parameters for the client request
        params = {"query": query}

        # --- Call the MCP client ---
        # 'result' contains whatever the MCP client layer returns after
        # communicating with the server and processing its response.
        result: Any = await mcp_client.process_query("sql_tool", params=params)

        print(f"--- Client Tool: sql_tool received result from mcp_client ---")
        print(f"   Result type: {type(result)}")
        # Log snippet for debugging, handle non-string types gracefully
        if isinstance(result, str):
            print(f"   Result snippet (str): {result[:500]}{'...' if len(result) > 500 else ''}")
        elif isinstance(result, (list, dict)):
            # Convert complex types to string for logging snippet
            print(f"Result is a list or dict")
            result_str_snippet = str(result)
            print(f"   Result snippet (list/dict): {result_str_snippet[:500]}{'...' if len(result_str_snippet) > 500 else ''}")
        else:
            print(f"   Result (other type)")
            result = parse_call_tool_result(result=result)
            print(result)

        final_output_str: str

        if isinstance(result, str):
            final_output_str = result
        elif isinstance(result, (dict, list)):
            try:
                # Convert dict or list to DataFrame
                if isinstance(result, dict):
                    df = pd.DataFrame.from_dict(result)
                else:  # list
                    df = pd.DataFrame(result)

                # Generate a random 10-character string
                random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
                # Construct the file path
                  # Replace with actual path
                file_path = os.path.join(SAVE_PATH_FILE, f"result_{random_string}.csv")
                print(file_path)
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                print("THIS IS THE FILE PATH: ", file_path)
                # Save DataFrame to CSV
                df.to_csv(file_path, index=False)
                print(f"   Saved DataFrame to CSV at: {file_path}")
                result_str = json.dumps(result)

                if isinstance(result, dict):
                    first_key = next(iter(result))
                    first_value = result[first_key]
                    if isinstance(first_value, list) and len(first_value) < 20:
                        final_output_str = f"The response from the server has been saved at {file_path}, and this is the result of the query: {result_str}"
                
                elif isinstance(result, list) and len(result) < 20:
                    final_output_str = f"The response from the server has been saved at {file_path}, and this is the result of the query: {result_str}"

                else:
                    snippet = result_str[:500] + ('...' if len(result_str) > 500 else '')
                    final_output_str = f"The response from the server is too long. See the full response at path {file_path}, this is only a snippet of the result: {snippet}"

            except Exception as conv_err:
                print(f"Warning: Could not process dict/list to DataFrame or save CSV: {conv_err}. Falling back to str().")
                final_output_str = str(result)  # Fallback to generic string representation
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

def parse_call_tool_result(result: Any) -> List[Dict]:
    try:
        # Check if result has a 'content' attribute
        if not hasattr(result, 'content'):
            raise ValueError("Input result does not have a 'content' attribute")

        result_list = []
        for content_item in result.content:
            # Check if content_item has a 'text' attribute
            if not hasattr(content_item, 'text'):
                raise ValueError("Content item does not have a 'text' attribute")
            try:
                str_json = content_item.text
                cleaned_json = handle_json(str_json)
                    
                parsed_dict = json.loads(cleaned_json)
                result_list.append(parsed_dict)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON from text: {content_item.text}. Error: {e}")

        return result_list

    except Exception as e:
        raise ValueError(f"Error processing CallToolResult: {str(e)}")