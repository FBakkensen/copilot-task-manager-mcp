"""Tests for the MCP server initialization."""

import pytest
from fastmcp import FastMCP

from copilot_task_manager.server.mcp_server import (  # noqa: E501
    TaskManagerMCPServer,
    create_server,
)


@pytest.fixture
def server() -> TaskManagerMCPServer:
    """Create a server instance for testing."""
    return create_server()


class TestMCPServerCreation:
    """Test suite for MCP server creation.

    Following BDD style:
    - Given the requirements for an MCP server
    - When the server is created
    - Then it should have the expected configuration
    """

    def test_create_server_with_default_name(self) -> None:
        """Test server creation with default name.

        Given the requirements for an MCP server
        When creating a server with default name
        Then it should be a TaskManagerMCPServer instance
        And have the default server name
        """
        # When
        server = create_server()

        # Then
        assert isinstance(server, TaskManagerMCPServer)
        assert server.server_name == 'TaskManagerServerV3'

    def test_create_server_with_custom_name(self) -> None:
        """Test server creation with custom name.

        Given the requirements for an MCP server
        When creating a server with a custom name
        Then it should be a TaskManagerMCPServer instance
        And have the specified custom name
        """
        # Given
        custom_name = 'CustomTaskServer'

        # When
        server = create_server(custom_name)

        # Then
        assert isinstance(server, TaskManagerMCPServer)
        assert server.server_name == custom_name


class TestMCPServerConfiguration:
    """Test suite for MCP server configuration.

    Following BDD style:
    - Given a newly created MCP server
    - When checking its configuration
    - Then it should have the expected components initialized
    """

    def test_server_has_mcp_instance_initialized(
        self,
        server: TaskManagerMCPServer,
    ) -> None:
        """Test that server has an MCP instance initialized.

        Given a newly created MCP server
        When checking its MCP instance
        Then it should have an MCP instance initialized
        """
        # Then
        assert hasattr(server, 'mcp')
        assert server.mcp is not None
        assert isinstance(server.mcp, FastMCP)

    def test_server_has_tools_setup_method(
        self,
        server: TaskManagerMCPServer,
    ) -> None:
        """Test that server has a method to setup MCP tools.

        Given a newly created MCP server
        When checking its tools setup method
        Then it should have a method to set up MCP tools
        """
        # Then
        assert hasattr(server, '_setup_tools')
        assert callable(server._setup_tools)

    def test_setup_tools_is_called_during_initialization(
        self, mocker: pytest.MonkeyPatch
    ) -> None:
        """Test that _setup_tools is called during initialization.

        Given the requirements for server initialization
        When a new server is created
        Then the _setup_tools method should be called
        """
        # Given
        mock_setup_tools = mocker.patch.object(
            TaskManagerMCPServer, '_setup_tools', autospec=True
        )

        # When
        server = create_server()

        # Then
        mock_setup_tools.assert_called_once_with(server)


class TestMCPServerLifecycle:
    """Test suite for MCP server lifecycle management.

    Following BDD style:
    - Given a newly created MCP server
    - When managing its lifecycle
    - Then it should support proper start and stop operations
    """

    @pytest.mark.asyncio
    async def test_server_has_lifecycle_methods(self) -> None:
        """Test that server has start and stop methods.

        Given a newly created MCP server
        When checking its lifecycle methods
        Then it should have start and stop methods
        """
        # Given
        server = create_server()

        # Then
        assert hasattr(server, 'start')
        assert hasattr(server, 'stop')
        assert callable(server.start)
        assert callable(server.stop)

    @pytest.mark.asyncio
    async def test_start_stop_methods_exist(self) -> None:
        """Test server start and stop methods work without exceptions.

        Given a newly created MCP server
        When using the start and stop methods
        Then they should execute without errors
        """
        # Given
        server = create_server()

        # When/Then - no exceptions should be raised
        await server.start()
        await server.stop()
