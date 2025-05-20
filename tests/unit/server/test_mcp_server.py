"""Tests for the MCP server initialization."""

import typing
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import FastMCP

from copilot_task_manager.server.mcp_server import (  # noqa: E501
    TaskManagerMCPServer,
    create_server,
)


@pytest.fixture  # type: ignore[misc]
def mocked_mcp(mocker: Any) -> Any:
    """Create a mocked FastMCP for all tests.

    Returns:
        MagicMock: A mocked FastMCP instance.
    """
    # Create async mock instance with async methods
    mock = MagicMock(spec=FastMCP)

    # Patch both async and sync start for compatibility
    async def async_start() -> None:
        pass

    mock.start = AsyncMock(side_effect=async_start)
    mock.stop = AsyncMock()

    # Mock FastMCP constructor to return our mock
    mcp_path = 'copilot_task_manager.server.mcp_server.FastMCP'
    mocker.patch(mcp_path, return_value=mock)

    return mock


@pytest.fixture  # type: ignore[misc]
def server(mocked_mcp: Any) -> Any:
    """Create a server instance for testing.

    All server instances will have a mocked FastMCP instance.
    """
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


class TestMCPServerErrorHandling:
    """Test suite for MCP server error handling.

    Following BDD style:
    - Given invalid server configuration
    - When attempting server operations
    - Then appropriate errors should be raised
    """

    @pytest.mark.parametrize(
        'name',
        ['', ' ', None, typing.cast(str, {})],  # type: ignore
    )
    def test_create_server_with_invalid_name(self, name: typing.Any) -> None:
        """Test server creation with invalid name.

        Given an invalid server name
        When attempting to create a server
        Then it should raise a ValueError
        """
        with pytest.raises(
            ValueError,
            match='Server name must be a non-empty string',
        ):
            create_server(typing.cast(str, name))

    @pytest.mark.parametrize(
        'port',
        [-1, 0, 65536, None, 'invalid'],  # type: ignore
    )
    def test_server_with_invalid_port(self, port: typing.Any) -> None:
        """Test port validation.

        Given invalid port values
        When attempting to set the port
        Then it should raise a ValueError
        """
        # Given
        server = create_server()

        # When/Then
        with pytest.raises(
            ValueError,
            match='Port must be between 1 and 65535',
        ):
            server.port = port


class TestMCPServerConfiguration:
    """Test suite for MCP server configuration.

    Following BDD style:
    - Given a newly created MCP server
    - When checking its configuration
    - Then it should have the expected settings
    """

    def test_server_default_configuration(
        self,
        server: TaskManagerMCPServer,
    ) -> None:
        """Test server default configuration values.

        Given a newly created MCP server
        When checking its configuration
        Then it should have the expected default values
        """
        # Then
        assert server.port == 3000  # Default MCP port
        assert server.host == 'localhost'  # Default host
        assert not server.debug  # Debug mode should be off by default

    def test_server_custom_configuration(self) -> None:
        """Test server with custom configuration.

        Given custom configuration values
        When creating a server with those values
        Then it should use the custom configuration
        """
        # Given
        server = create_server(
            'CustomServer',
            port=3001,
            host='127.0.0.1',
            debug=True,
        )

        # Then
        assert server.server_name == 'CustomServer'
        assert server.port == 3001
        assert server.host == '127.0.0.1'
        assert server.debug is True

    @pytest.mark.asyncio  # type: ignore[misc]
    async def test_server_runtime_configuration_changes(
        self,
        server: Any,
    ) -> None:
        """Test server configuration changes at runtime.

        Given a running server
        When changing configuration at runtime
        Then it should handle changes appropriately
        """
        # Given
        await server.start()

        # When/Then - Should not allow port change while running
        with pytest.raises(
            RuntimeError,
            match='Cannot change port while server is running',
        ):
            server.port = 3001

        await server.stop()

        # When/Then - Should allow port change when stopped
        server.port = 3001
        assert server.port == 3001

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
        self,
        mocker: pytest.MonkeyPatch,
    ) -> None:
        """Test that _setup_tools is called during initialization.

        Given the requirements for server initialization
        When a new server is created
        Then the _setup_tools method should be called
        """
        # Given
        mock_setup_tools = mocker.patch.object(
            TaskManagerMCPServer,
            '_setup_tools',
            autospec=True,
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

    @pytest.mark.asyncio  # type: ignore[misc]
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

    @pytest.mark.asyncio  # type: ignore[misc]
    async def test_start_stop_methods_exist(
        self,
        server: Any,
    ) -> None:
        """Test server start and stop methods work without exceptions.

        Given a newly created MCP server
        When using the start and stop methods
        Then they should execute without errors
        """
        # When/Then - no exceptions should be raised
        await server.start()
        await server.stop()

    @pytest.mark.asyncio  # type: ignore[misc]
    async def test_server_lifecycle_state(
        self,
        server: Any,
    ) -> None:
        """Test server lifecycle state management.

        Given a newly created MCP server
        When starting and stopping the server
        Then it should properly track its running state
        """
        # Given
        assert not server._is_running

        # When starting
        await server.start()
        # Then should be running
        assert server._is_running

        # When stopping
        await server.stop()
        # Then should not be running
        assert not server._is_running
