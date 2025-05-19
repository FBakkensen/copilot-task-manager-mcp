"""Main entry point for running the Copilot Task Manager MCP server."""

import asyncio
import logging
import signal
import sys
from typing import Any, Callable

from .mcp_server import create_server


def setup_logging() -> None:
    """Configure logging for the server."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


def handle_shutdown(
    server: Any, loop: asyncio.AbstractEventLoop
) -> Callable[[Any, Any], None]:
    """Create a shutdown handler.

    Args:
        server: The MCP server instance.
        loop: The asyncio event loop.

    Returns:
        Callable: A signal handler function.
    """

    def _handler(*args: Any) -> None:
        """Handle shutdown signals.

        Args:
            *args: Signal arguments (unused).
        """
        logging.info('Shutting down MCP server...')
        asyncio.create_task(server.stop())
        loop.stop()
        sys.exit(0)

    return _handler


def main() -> None:
    """Run the MCP server."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info('Starting Task Manager MCP Server...')

    server = create_server()
    loop = asyncio.get_event_loop()

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown(server, loop))
    signal.signal(signal.SIGTERM, handle_shutdown(server, loop))

    try:
        loop.run_until_complete(server.start())
        loop.run_forever()
    except Exception as e:
        logger.error(f'Server error: {e}')
        sys.exit(1)
    finally:
        loop.close()


if __name__ == '__main__':
    main()
