"""MCP Server for Copilot Task Manager.

This module implements a FastMCP server that provides task management
functionality through the Model Context Protocol (MCP).
"""

from fastmcp import FastMCP


class TaskManagerMCPServer:
    """MCP server implementation for task management."""

    def __init__(self, server_name: str = 'TaskManagerServerV3') -> None:
        """Initialize the MCP server.

        Args:
            server_name (str): The name of the MCP server instance.
        """
        self.server_name = server_name
        self.mcp = FastMCP(server_name)
        self._setup_tools()

    def _setup_tools(self) -> None:
        """Register all MCP tools with their handlers."""
        # Tools will be registered here in future steps

    async def start(self) -> None:
        """Start the MCP server."""
        await self.mcp.start()

    async def stop(self) -> None:
        """Stop the MCP server."""
        await self.mcp.stop()


def create_server(
    server_name: str = 'TaskManagerServerV3',
) -> TaskManagerMCPServer:
    """Create a new instance of the TaskManagerMCPServer.

    Args:
        server_name (str): The name of the MCP server instance.

    Returns:
        TaskManagerMCPServer: A new server instance.
    """
    return TaskManagerMCPServer(server_name)
