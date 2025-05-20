"""Main entry point for the MCP Server.

This script initializes and runs the MCP Server with configuration options.
"""

import argparse
import asyncio
import os
from typing import Optional

from mcp_server.server import DataServer
from mcp_server.tools.db_tools import create_db_engine, get_db_structure

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the MCP Server")
    
    # Server configuration
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0", 
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to"
    )
    parser.add_argument(
        "--transport", 
        type=str, 
        default="sse", 
        choices=["stdio", "sse"], 
        help="Transport protocol to use"
    )
    
    # Database configuration
    parser.add_argument(
        "--connection_string", 
        type=str, 
        help="Database host (overrides environment variable)"
    )
    
    return parser.parse_args()

def get_db_info(connection_string):
    """Get database information asynchronously."""
    engine = create_db_engine(connection_string)
    structure = get_db_structure(engine, "public")

def main():
    """Main entry point."""
    args = parse_args()
    
    # Handle database operations if needed
    if args.connection_string:
        # Run the async database operations in a separate event loop
        get_db_info(args.connection_string)
    
    # Create server
    server = DataServer(
        name="DataServer",
        instructions="I am a data server that provides tools for data querying, visualization, machine learning, and Python code execution.",
        host=args.host,
        port=args.port,
    )
    
    # Run server (synchronous operation)
    print(f"Starting MCP Server on {args.host}:{args.port} using {args.transport} transport")
    server.run(transport=args.transport)

if __name__ == "__main__":
    main() 

