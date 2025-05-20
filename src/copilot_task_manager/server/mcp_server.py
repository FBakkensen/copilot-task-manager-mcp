"""MCP Server for Copilot Task Manager.

This module implements a FastMCP server that provides task management
functionality through the Model Context Protocol (MCP).
"""

from typing import Any

from fastmcp import FastMCP


class TaskManagerMCPServer:
    """MCP server implementation for task management."""

    def __init__(
        self,
        server_name: str = 'TaskManagerServerV3',
        *,
        port: int = 3000,
        host: str = 'localhost',
        debug: bool = False,
    ) -> None:
        """Initialize the MCP server.

        Args:
            server_name (str): The name of the MCP server instance.
            port (int, optional): Port to run the server on. Defaults to 3000.
            host (str, optional): Host to bind to. Defaults to 'localhost'.
            debug (bool, optional): Enable debug mode. Defaults to False.

        Raises:
            ValueError: If server_name is empty or invalid.
        """
        self._validate_server_name(server_name)
        self.server_name = server_name
        self._port = port
        self._host = host
        self._debug = debug
        self._is_running = False
        self.mcp = FastMCP(server_name)
        self._setup_tools()

    @staticmethod
    def _validate_server_name(name: Any) -> None:
        """Validate server name.

        Args:
            name (Any): Server name to validate.

        Raises:
            ValueError: If name is invalid.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError('Server name must be a non-empty string')

    @property
    def port(self) -> int:
        """Get server port.

        Returns:
            int: Current port number.
        """
        return self._port

    @port.setter
    def port(self, value: Any) -> None:
        """Set server port.

        Args:
            value (Any): Port number to set.

        Raises:
            ValueError: If port is invalid.
            RuntimeError: If changing port while server is running.
        """
        if self._is_running:
            raise RuntimeError('Cannot change port while server is running')
        if not isinstance(value, int) or not 1 <= value <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        self._port = value

    @property
    def host(self) -> str:
        """Get server host.

        Returns:
            str: Current host.
        """
        return self._host

    @property
    def debug(self) -> bool:
        """Get debug mode.

        Returns:
            bool: Current debug mode.
        """
        return self._debug

    def _setup_tools(self) -> None:
        """Register all MCP tools with their handlers."""
        # Tools will be registered here in future steps

    async def start(self) -> None:
        """Start the MCP server.

        Raises:
            ValueError: If port is invalid.
        """
        if not isinstance(self.port, int) or not 1 <= self.port <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        self._is_running = True
        # Note: FastMCP doesn't have start/stop yet, will be implemented
        # in the MCP implementation step

    async def stop(self) -> None:
        """Stop the MCP server."""
        self._is_running = False
        # Note: FastMCP doesn't have start/stop yet, will be implemented
        # in the MCP implementation step


def create_server(
    server_name: str = 'TaskManagerServerV3',
    *,
    port: int = 3000,
    host: str = 'localhost',
    debug: bool = False,
) -> TaskManagerMCPServer:
    """Create a new instance of the TaskManagerMCPServer.

    Args:
        server_name (str): The name of the MCP server instance.
        port (int, optional): Port to run the server on. Defaults to 3000.
        host (str, optional): Host to bind to. Defaults to 'localhost'.
        debug (bool, optional): Enable debug mode. Defaults to False.

    Returns:
        TaskManagerMCPServer: A new server instance.

    Raises:
        ValueError: If server_name is empty or invalid.
    """
    return TaskManagerMCPServer(
        server_name,
        port=port,
        host=host,
        debug=debug,
    )
