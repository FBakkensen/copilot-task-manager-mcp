Technical Design Document: Copilot Task Manager MCP Server
Version: 1.0
Date: May 19, 2025
Author: Award-Winning Writer AI

1. Introduction
1.1. Purpose
This document provides the technical design for the Copilot Task Manager MCP Server. It details the system architecture, data model, MCP tool specifications, and other technical aspects necessary for its implementation.

1.2. Scope
The scope covers the design of a Python-based local MCP server that integrates with GitHub Copilot Chat in VS Code. It includes persistent storage using SQLite and an "active project" memory feature. Future UI integration considerations are also discussed.

2. System Architecture
2.1. Overview
The system is a local MCP server designed to run on the user's machine. GitHub Copilot in VS Code acts as the MCP client, sending requests to this server based on user prompts in the chat interface. The server processes these requests, interacts with a local SQLite database for data persistence, and returns results to Copilot.
+---------------------------+      (JSON-RPC via stdio)      +--------------------------+
| GitHub Copilot Chat | &lt;----------------------------> | Python MCP Server |
| (VS Code - MCP Client) | | (FastMCP, Active Project |
+---------------------------+ | State, Tool Logic) |
+------------+-------------+
| (SQL)
+------------V-------------+
| SQLite Database |
| (tasks.db: Projects, |
| Tasks tables) |
+--------------------------+


### 2.2. Components
*   **Python MCP Server (`server.py`):**
    *   Built using the `FastMCP` library. [1, 2]
    *   Defines and exposes MCP tools.
    *   Manages in-memory state for the "active project" (`_active_project_name`, `_active_project_id`).
    *   Handles incoming JSON-RPC requests from the MCP client (Copilot).
    *   Orchestrates calls to the Database Module.
    *   Formats responses (strings) for Copilot.
    *   Includes error handling and logging.
*   **Database Module (`database.py`):**
    *   Encapsulates all interactions with the SQLite database.
    *   Provides functions for CRUD (Create, Read, Update, Delete) operations on `Projects` and `Tasks` tables.
    *   Handles database connection management and schema initialization.
*   **SQLite Database (`tasks.db`):**
    *   A single file storing all persistent data for projects and tasks.

### 2.3. Technology Stack
*   **Programming Language:** Python 3.10+ [3]
*   **MCP Server Library:** `FastMCP` (part of `mcp[cli]`) [1, 2]
*   **Database:** SQLite 3 (via Python's built-in `sqlite3` module) [4]
*   **Development Environment:** VS Code
*   **Interaction Client:** GitHub Copilot Chat in VS Code [5, 6]

## 3. Data Design

### 3.1. Database Choice
SQLite is chosen for its serverless, file-based nature, ease of integration with Python, and sufficient capabilities for a local, single-user application. [4]

### 3.2. Schema Definition

**Table: `Projects`**
*   `project_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the project.
*   `project_name` (TEXT, UNIQUE, NOT NULL): User-defined name for the project.
*   `created_at` (TEXT, DEFAULT CURRENT_TIMESTAMP): Timestamp of project creation.

**SQL:**
```sql
CREATE TABLE IF NOT EXISTS Projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
Table: Tasks

task_id (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the task.
project_id (INTEGER, NOT NULL): Foreign key referencing Projects.project_id.
description (TEXT, NOT NULL): Textual description of the task.
status (TEXT, NOT NULL, DEFAULT 'open'): Current status ('open', 'completed').
priority (INTEGER, NULLABLE): Optional numerical priority.
due_date (TEXT, NULLABLE): Optional due date (ISO8601 format: "YYYY-MM-DD").
created_at (TEXT, DEFAULT CURRENT_TIMESTAMP): Timestamp of task creation.
updated_at (TEXT, DEFAULT CURRENT_TIMESTAMP): Timestamp of last task update.
SQL:

SQL

CREATE TABLE IF NOT EXISTS Tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open', -- 'open' or 'completed'
    priority INTEGER,
    due_date TEXT, -- Store as YYYY-MM-DD
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects (project_id) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS update_task_updated_at
AFTER UPDATE ON Tasks
FOR EACH ROW
BEGIN
    UPDATE Tasks SET updated_at = CURRENT_TIMESTAMP WHERE task_id = OLD.task_id;
END;
The ON DELETE CASCADE for the foreign key ensures that if a project is deleted, all its associated tasks are also automatically deleted.

4. MCP Server Design
4.1. MCP Tool Definitions
The server will expose the following tools. Each tool is defined by its name, a natural language description (critical for LLM understanding ), input parameters, and return type.

(See API Specification document for detailed breakdown of each tool)

createProjectList(projectName: str) -> str
setActiveProject(projectName: str) -> str
addTask(taskDescription: str, projectName: Optional[str] = None, priority: Optional[int] = None, dueDate: Optional[str] = None) -> str
listTasks(projectName: Optional[str] = None, statusFilter: str = 'open') -> str
markTaskComplete(taskIdOrDescription: str, projectName: Optional[str] = None) -> str
removeTask(taskIdOrDescription: str, projectName: Optional[str] = None) -> str
4.2. Active Project State Management
The server.py module will maintain two global variables:

_active_project_name: Optional[str] = None
_active_project_id: Optional[int] = None
These variables are updated by the setActiveProject tool. A helper function, _get_current_project_context(provided_project_name: Optional[str]), will be used by other tools to:

Check if provided_project_name is given. If so, fetch its ID from the database.
If not, use _active_project_name and _active_project_id.
If neither is available, return an error state. This state is session-specific and will be reset if the Python server restarts.
4.3. Error Handling
Database Layer (database.py): Functions will use try-except sqlite3.Error blocks to catch SQLite-specific errors. They will log errors and return None or False to indicate failure to the calling tool function.
Tool Layer (server.py): Each MCP tool function will use try-except Exception blocks to catch errors from the database layer or other unexpected issues. They will log these errors and return user-friendly string messages to Copilot (e.g., "Error: Project 'X' not found.").
4.4. Output Formatting
Most tools will return simple string confirmation or error messages.
The listTasks tool will format its output as a multi-line string, with each task on a new line, mimicking markdown to-do list syntax (e.g., [ ] Task (ID: 1)..., [x] Task (ID: 2)...). This aids readability in the Copilot Chat interface.
## 5. Future UI Integration Considerations

If a dedicated VS Code extension UI (e.g., Tree View or Webview) is developed in the future, several architectural approaches can be considered:

### 5.1. Architectural Approaches

#### VS Code Extension (TypeScript) with a Local API on Python Server

- The Python MCP server is augmented to also expose a simple local HTTP/REST API (e.g., using Flask/FastAPI)
- The VS Code extension (TypeScript) acts as a client to this local HTTP API to fetch data and trigger actions
- The Python server continues to be the single source of truth for database interactions
- The VS Code extension could manage the lifecycle of the Python server process

**Pros:** Reuses existing Python logic; clear separation
**Cons:** Introduces inter-process communication (IPC) for UI; Python server needs dual interfaces (MCP and HTTP)

#### Full TypeScript VS Code Extension

- Re-implement the core task management logic (including SQLite interaction using a Node.js library like sqlite3) directly within the VS Code extension in TypeScript
- The MCP interaction for Copilot Chat would then be handled by an "Agent Mode Tool" contributed by this same VS Code extension, rather than an external MCP server

**Pros:** Unified codebase in TypeScript; tighter integration with VS Code APIs; no separate Python process
**Cons:** Requires rewriting backend logic; loses Python backend if preferred

#### Hybrid (Language Server Protocol - LSP)

- The Python backend could be structured as a Language Server
- The VS Code extension acts as a Language Client

**Pros:** Standardized protocol for rich client-server communication
**Cons:** Potentially overkill for this application; LSP is primarily designed for language-specific features

### 5.2. Impact on Current Design

- **Database Abstraction:** The current database.py provides a good abstraction. Its functions' signatures could serve as a blueprint if porting to TypeScript.
- **API Design:** If exposing an HTTP API from the Python server (Option 1), the current tool functions offer a good starting point for defining API endpoints.
- **State Management:** The "active project" state, currently in Python server memory, would need careful handling. For Option 1, the UI might need its own way to query/set this or the API would need endpoints for it. For Option 2, state would be managed within the TypeScript extension.

The choice of approach will depend on future requirements, desired level of VS Code integration, and development preferences. The current MCP server design provides a functional backend that can be built upon or adapted.