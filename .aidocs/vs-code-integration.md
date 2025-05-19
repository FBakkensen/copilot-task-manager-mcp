VS Code Integration Guide: Copilot Task Manager MCP Server
Version: 1.0
Date: May 19, 2025

This guide explains how to set up and use the Copilot Task Manager MCP server with GitHub Copilot Chat in Visual Studio Code.

1. Prerequisites
Python: Version 3.10 or higher installed.
VS Code: Latest version installed.
GitHub Copilot Subscription: Active Copilot subscription (Free, Pro, or Business).
GitHub Copilot Extension: GitHub Copilot and GitHub Copilot Chat extensions installed and enabled in VS Code.
MCP Enabled in VS Code: Ensure chat.mcp.enabled setting is true in VS Code (default).
2. Server Setup
2.1. Python Environment
Create a project directory (e.g., copilot_task_mcp_server_v3).
Navigate into the directory and create a Python virtual environment:
Bash

python -m venv.venv
Activate the virtual environment:
macOS/Linux: source.venv/bin/activate
Windows (PowerShell): .\.venv\Scripts\Activate.ps1
Windows (CMD): .\.venv\Scripts\activate.bat
2.2. Dependencies
With the virtual environment activated, install the required package:
Bash

pip install "mcp[cli]"
This installs FastMCP and its dependencies.
Place the server.py and database.py files (as provided in the Technical Design Document) into your project directory.
2.3. Running the Server
Ensure your virtual environment is active.
Navigate to your project directory in the terminal.
Run the server:
Bash

python server.py
The server will start, initialize the tasks.db database file (if it doesn't exist), and begin listening for MCP connections (typically via stdio when launched by VS Code, or on a default port if run standalone for testing with other tools). You should see log output like "Starting Task Manager MCP Server...".
3. VS Code Configuration (.vscode/mcp.json)
To make VS Code and Copilot aware of your local MCP server:

In your project's root directory (e.g., copilot_task_mcp_server_v3), create a folder named .vscode.

Inside the .vscode folder, create a file named mcp.json.

Add the following configuration to mcp.json, replacing placeholders with absolute paths specific to your system:

JSON

{
    "servers": {
        "TaskManagerServerV3": {
            "command":,
            "description": "Local MCP Server for Task Management (V3 with Active Project & UI Considerations).",
            "workingDirectory": "/full/path/to/your/project/" // ABSOLUTE path to project root
        }
    }
}
TaskManagerServerV3: This key must match the name used in mcp = FastMCP("TaskManagerServerV3") in your server.py.
command: An array. The first element is the absolute path to the Python interpreter within your virtual environment. The second element is the absolute path to your server.py script.
workingDirectory: The absolute path to the root of your server project directory. This is where tasks.db will be created/accessed.
Save the mcp.json file. VS Code should automatically detect this configuration if the MCP features are enabled. You might need to restart VS Code or use the "MCP: List Servers" command from the Command Palette (Ctrl+Shift+P) to verify.

## 4. Interacting with Copilot Chat

Once the server is running (either manually started by you, or automatically by VS Code based on the mcp.json configuration) and VS Code recognizes it:

1. **Open Copilot Chat:** In VS Code, open the Copilot Chat view (usually an icon in the Activity Bar or via `Ctrl+Alt+I`).
2. **Ensure Agent Mode** _(Optional but Recommended):_ While tools can be invoked directly, Agent Mode in Copilot Chat is often best for complex interactions or when you want Copilot to reason about which tool to use. You can select "Agent" from the chat mode selector.
3. **Invoke Tools:**
   - **Mentioning the Server:** Prefix your command with @ followed by the server name from mcp.json.
     Example: `@TaskManagerServerV3 create project list for "My Website"`
   - **Natural Language:** Copilot's agent mode may automatically select the appropriate tool from your server if your prompt clearly matches a tool's description.
     Example: `"add a high priority task to My Website to deploy the new homepage by tomorrow"`
   - **Direct Tool Invocation:** You can sometimes directly reference tools using #toolName (e.g., `#addTask`).

### 4.1. Example Prompts

| Action | Command |
|--------|---------|
| Create a project | `@TaskManagerServerV3 create project "Alpha Project"` |
| Set active project | `@TaskManagerServerV3 set active project to "Alpha Project"` |
| Add a task to the active project | `@TaskManagerServerV3 add task "Design the login page" priority 1 due 2025-06-15` |
| Add a task to a specific project | `@TaskManagerServerV3 add task to "Beta Project": "Setup CI/CD pipeline"` |
| List open tasks for active project | `@TaskManagerServerV3 list tasks` |
| List completed tasks for a project | `@TaskManagerServerV3 list tasks for "Alpha Project" status completed` |
| Mark a task complete (by description) | `@TaskManagerServerV3 mark task "Design the login page" complete` |
| Mark a task complete (by ID) | `@TaskManagerServerV3 mark task ID 5 complete` |
| Remove a task | `@TaskManagerServerV3 remove task "Setup CI/CD pipeline"` |

### 4.2. Tips

- **Tool Discovery:** In Copilot Chat (Agent Mode), you can often click a "Tools" icon or similar to see available tools from configured MCP servers, including yours.
- **Clarity is Key:** The more clearly you phrase your request, the better Copilot can match it to the correct tool and extract parameters. Refer to the tool descriptions if unsure.
- **Confirmation:** Copilot may ask for confirmation before executing actions from your local server, especially initially.

This setup provides a powerful way to integrate custom task management directly into your development workflow using GitHub Copilot.
