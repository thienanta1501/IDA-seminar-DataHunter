import asyncio
import json
import os
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client
from dotenv import load_dotenv


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_sse_server(self, server_url: str):
        """Connect to an MCP server running with SSE transport"""
        print(f"Connecting to server at {server_url}")
        # Store the context managers so they stay alive
        self._streams_context = sse_client(url=server_url)
        streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*streams)
        print(f"Session context: {self._session_context}")
        self.session: ClientSession = await self._session_context.__aenter__()

        # Initialize
        await self.session.initialize()

        # List available tools to verify connection
        print("Initialized SSE client...")
        print("Listing tools...")
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if hasattr(self, "_session_context") and self._session_context is not None:
            try:
                await self._session_context.__aexit__(None, None, None)
            except Exception as e:
                print(f"Error closing session_context: {e}")

        if hasattr(self, "_streams_context") and self._streams_context is not None:
            try:
                await self._streams_context.__aexit__(None, None, None)
            except Exception as e:
                print(f"Error closing streams_context: {e}")

        self._session_context = None
        self._streams_context = None

    async def process_query(self, query: str, params: dict = None) -> str:
        print("Da vao session call tool")
        result = await self.session.call_tool(query, params)

        return result



mcp_client = None

async def get_mcp_client():
    global mcp_client
    print(f"bien mcp global luc nay la: ", mcp_client)
    if mcp_client is None:
        mcp_client = MCPClient()
        await mcp_client.connect_to_sse_server(server_url="http://localhost:8000/sse")
    print(f"bien mcp global sau if la: ", mcp_client)
    return mcp_client

async def delete_mcp_client():
    global mcp_client
    if mcp_client is not None:
        await mcp_client.cleanup()
        mcp_client = None
    print(f"mcp sau khi delete la: ", mcp_client)


