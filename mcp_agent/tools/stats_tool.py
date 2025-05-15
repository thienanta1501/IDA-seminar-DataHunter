"""Statistic tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
statistic tools.
"""
OUTPUT_DIRECTORY = r'C:\Users\Admin\Project_C\StatsTool'

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import pandas as pd
from mcp_agent.mcp_client import get_mcp_client
import json

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
                parsed_dict = json.loads(content_item.text)
                result_list.append(parsed_dict)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON from text: {content_item.text}. Error: {e}")

        return result_list

    except Exception as e:
        raise ValueError(f"Error processing CallToolResult: {str(e)}")
    
async def generate_html_report(
    data_source: str,
    output_html_file: str,
    date_cols: Optional[List[str]] = None,
    cat_threshold: int = 20,
    id_cols: Optional[List[str]] = None,
    report_title: str = "Data Analysis Report"
):
    """
    Generate a full statistical HTML report from a CSV file. Use this tool when query result has been saved before

    This function reads data from the given CSV file, analyzes its structure, computes statistics 
    (min, max, mean, std, missing values, etc.), plots distributions and correlations, 
    then compiles everything into a single HTML report.

    Args:
        file_path (str): Path to the CSV or Excel file containing the dataset.
        output_html_file (str): Path where the generated HTML report will be saved.
        date_cols (List[str], optional): Columns to parse as dates.
        cat_threshold (int, optional): Threshold for categorical detection.
        id_cols (List[str], optional): List of ID columns to exclude from analysis.
        report_title (str, optional): Title for the report. Defaults to "Data Analysis Report".

    Returns:
        Html content returned from the MCP server after invoking the report tool.

    """
    try:
        mcp_client = await get_mcp_client()
        tool_name = "generate_html_report"
        params = {
            "data_source": data_source,
            "date_cols": date_cols,
            "cat_threshold": cat_threshold,
            "id_cols": id_cols,
            "report_title": report_title
        }

        
        result = await mcp_client.process_query(tool_name, params=params)
        content = result.content
        str_content = ''.join(str(c.text).replace('\n', '') for c in content)
        output_html_file = OUTPUT_DIRECTORY + '\\' + output_html_file
        with open(output_html_file, 'w', encoding='utf-8') as f:
            f.write(str_content)
        return f"Output file saved at: {output_html_file}"

    except Exception as e:
        print(f"Error when calling tool generate_html_report: {e}")
        return f"Exception when calling generate_html_report tool: {e}"
