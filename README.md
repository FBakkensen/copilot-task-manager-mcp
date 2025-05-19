# Copilot Task Manager MCP

A Task Manager Model Context Protocol (MCP) server for managing tasks within Visual Studio Code.

## Description

This project implements a Model Context Protocol (MCP) server that provides task management functionality. It allows users to create, manage, and track tasks directly within Visual Studio Code through the MCP protocol.

## Features

- Task creation, management, and tracking
- MCP protocol integration
- Visual Studio Code integration
- Task persistence
- Scheduling and notifications (planned)

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS

# Install dependencies using Poetry
poetry install
```

## Development

This project uses Poetry for dependency management and packaging. Development dependencies include:
- pytest for testing
- black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

## License

[MIT License](LICENSE)
