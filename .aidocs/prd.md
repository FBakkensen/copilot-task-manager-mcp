Product Requirements Document: Copilot Task Manager MCP Server
Version: 1.0
Date: May 19, 2025
Author: Award-Winning Writer AI

# 1. Introduction
## 1.1. Purpose
This document outlines the product requirements for a local Model Context Protocol (MCP) server designed to function as a task management system. This system will be primarily interacted with through GitHub Copilot Chat within the Visual Studio Code (VS Code) environment, providing developers with a seamless way to manage project-specific tasks directly within their IDE.

## 1.2. Scope
The scope of this project includes the design, development, and deployment of a Python-based MCP server. Key functionalities include managing multiple task lists (one per project), persistent storage of tasks, and an "active project" feature to streamline user interaction. The server will expose its functionalities as tools discoverable and invocable by GitHub Copilot. This document also considers future integration with a dedicated VS Code extension UI.

## 1.3. Goals & Objectives
**Primary Goal:** To provide developers with a simple, efficient, and integrated task management solution within their VS Code environment via GitHub Copilot Chat.
**Objectives:**
- Develop a local MCP server for task management.
- Support multiple projects, each with its own task list.
- Implement persistent storage for all project and task data.
- Introduce an "active project" context to simplify commands.
- Ensure seamless integration with GitHub Copilot Chat.
- Design the system with future extensibility in mind, particularly for a potential VS Code UI.
- Provide clear, markdown-like task display within the chat interface.

# 2. Target Audience
The primary target audience for this product is:

- **Software Developers:** Individual developers or small teams who use VS Code and GitHub Copilot and require a lightweight, integrated solution for managing development-related tasks and to-do lists for different projects.
- **Users of GitHub Copilot Chat:** Individuals looking to extend Copilot's capabilities with custom tools for personal productivity.

# 3. User Stories
- As a developer, I want to create a new task list for a new project so that I can start organizing tasks specific to that project.
- As a developer, I want to set an active project so that I don't have to specify the project name for every subsequent task command.
- As a developer, I want to add a new task to the active project (or a specified project) with a description, optional priority, and optional due date, so I can keep track of what needs to be done.
- As a developer, I want to list all open tasks for the active project (or a specified project) so I can see what I need to work on.
- As a developer, I want to list all completed tasks for a project so I can review what has been accomplished.
- As a developer, I want to list all tasks (both open and completed) for a project for a comprehensive overview.
- As a developer, I want to mark a task in the active project (or a specified project) as complete by its ID or description, so I can update its status.
- As a developer, I want to remove a task from the active project (or a specified project) by its ID or description, so I can clean up my task list.
- As a developer, I want my tasks and projects to be saved persistently so that I don't lose my data when the server or VS Code restarts.
- As a developer, I want to interact with my task manager using natural language commands in GitHub Copilot Chat.
- As a developer, I want the task list displayed in Copilot Chat to be clear and easy to read, similar to a markdown to-do list.

# 4. Product Features & Functional Requirements
## 4.1. Core Task Management
- **FR1.1 Add Task:** The system shall allow users to add a new task with a textual description.
- **FR1.2 Task Attributes:** Tasks can optionally have a numerical priority and a due date (formatted as YYYY-MM-DD).
- **FR1.3 Task Status:** Tasks shall have a status, defaulting to "open". Other statuses include "completed".
- **FR1.4 Mark Task Complete:** The system shall allow users to change a task's status to "completed".
- **FR1.5 Remove Task:** The system shall allow users to remove a task.
- **FR1.6 List Tasks:** The system shall allow users to list tasks.
  - **FR1.6.1 Filter by Status:** Task listing shall support filtering by status ("open", "completed", "all"). Default is "open".
  - **FR1.6.2 Markdown-like Display:** Listed tasks should be formatted in a clear, markdown-like style (e.g., [ ] Task description, [x] Completed task).
- **FR1.7 Task Identification:** Tasks can be identified for completion or removal by their system-generated unique ID or by a unique portion of their description (prioritizing open tasks for description-based modification).

## 4.2. Project Management
- **FR2.1 Create Project List:** The system shall allow users to create a new, uniquely named project list.
- **FR2.2 Multiple Projects:** The system shall support managing tasks across multiple distinct projects. Each task must belong to a project.

## 4.3 Active Project Context

#### FR3.1 Set Active Project
The system shall allow users to set an existing project as the "active project".

#### FR3.2 Active Project Memory
The server shall remember the active project for the duration of its current session.

#### FR3.3 Implicit Project Operations
Task operations (add, list, complete, remove) shall default to using the active project if no specific project name is provided in the command.

#### FR3.4 Override Active Project
Users can specify a project name in a task operation command to override the active project for that specific command.

#### FR3.5 Active Project Requirement
If no project name is specified for a task operation and no active project is set, the system shall return an error.

## 4.4 MCP Server & Copilot Integration

#### FR4.1 MCP Server Implementation
The system shall be implemented as a local MCP server using Python and the FastMCP library.

#### FR4.2 MCP Tool Exposure
All core functionalities (create project, set active project, add task, list tasks, mark complete, remove task) shall be exposed as distinct tools via MCP.

#### FR4.3 Tool Definitions
Each MCP tool shall have a clear name, a detailed description for LLM understanding, and defined parameters (with types and optionality).

#### FR4.4 Copilot Chat Interaction
Users shall be able to invoke these tools using natural language prompts in GitHub Copilot Chat within VS Code.

#### FR4.5 VS Code Configuration
The system shall be configurable in VS Code via `.vscode/mcp.json` or user settings for local server discovery.

## 4.5 Data Persistence

#### FR5.1 Persistent Storage
All project and task data (including names, descriptions, statuses, priorities, due dates, and relationships) shall be stored persistently.

#### FR5.2 SQLite Database
SQLite shall be used as the database engine for persistent storage.

#### FR5.3 Data Integrity
The database schema shall enforce relationships (e.g., tasks belong to projects) and uniqueness where appropriate (e.g., project names).

# 5. Non-Functional Requirements

## 5.1 Usability

#### NFR1.1 Intuitive Interaction
Interaction via Copilot Chat should feel natural and require minimal learning for common operations.

#### NFR1.2 Clear Feedback
The server shall provide clear and concise confirmation messages or error messages for all operations.

#### NFR1.3 Reduced Repetition
The "active project" feature should significantly reduce the need for users to repeatedly type project names.

## 5.2 Performance

#### NFR2.1 Responsiveness
For a local server managing a personal number of tasks, operations should feel instantaneous (e.g., responses within 1-2 seconds for typical commands).

#### NFR2.2 Scalability (Local)
The system should handle several dozen projects and hundreds of tasks per project without noticeable degradation in performance for a single user.

## 5.3 Reliability

#### NFR3.1 Data Safety
Persistent storage should ensure that task data is not lost due to server restarts or normal application closure.

#### NFR3.2 Error Handling
The server should gracefully handle invalid inputs or unexpected situations and provide informative error messages.

## 5.4 Maintainability

#### NFR4.1 Modular Code
The Python codebase should be well-structured with clear separation of concerns (e.g., MCP tool logic, database interaction logic).

#### NFR4.2 Readability
Code should be clean, well-commented, and easy to understand for future development.

## 5.5 Security (for local server)

#### NFR5.1 Local Operation
The server is intended for local use. No external network exposure is required by default.

#### NFR5.2 Input Sanitization (Basic)
While not externally exposed, basic checks on input parameters for MCP tools are good practice.

# 6. Future Considerations
- **FC1. Enhanced Task Queries & Editing:**
  - Support for more complex filtering (date ranges, text search).
  - Sorting options for task lists.
  - An editTask tool.
- **FC2. VS Code Extension UI:**
  - Develop a dedicated VS Code extension with a graphical UI (e.g., Tree View in the sidebar, custom Webview) for managing tasks, potentially interacting with the Python backend via a local API or by reimplementing logic in TypeScript.
- **FC3. Context Awareness (Advanced Copilot Integration):**
  - Infer active project from VS Code workspace or Git repository context.
  - Link tasks to specific files or code lines.
- **FC4. Persistence of Active Project:**
  - Save the active project setting across server restarts.
- **FC5. getActiveProject Tool:**
  - A tool to allow users to query the currently set active project.
- **FC6. Sub-tasks:**
  - Support for hierarchical task structures.
