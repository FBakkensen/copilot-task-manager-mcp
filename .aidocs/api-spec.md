API Specification (MCP Tools): Copilot Task Manager
Version: 1.0
Date: May 19, 2025

This document specifies the interface for the MCP tools provided by the Copilot Task Manager server. Communication is based on JSON-RPC 2.0, as standard for MCP.

Tools
1. createProjectList
Description (for LLM): "Creates a new, empty task list for a given project name. Use this when a user wants to start tracking tasks for a new project or initialize a task list for an existing project name that doesn't have one yet."
Request Parameters:
projectName (string, required): "The unique name of the project for which to create a task list."
Response (string):
Success: "Project list '{projectName}' created successfully with ID: {project_id}."
Error: "Error: Project name cannot be empty." or "Error: Project list '{projectName}' already exists (ID: {project_id})." or "Error: Could not create project list '{projectName}'...."
2. setActiveProject
Description (for LLM): "Sets the currently active project for subsequent task operations. Once set, other commands like addTask or listTasks will use this project by default unless a specific project name is provided in those commands. The project must exist."
Request Parameters:
projectName (string, required): "The name of the project to set as active."
Response (string):
Success: "Project '{projectName}' is now the active project."
Error: "Error: Project name cannot be empty." or "Error: Project '{projectName}' not found. Cannot set as active."
3. addTask
Description (for LLM): "Adds a new task. If projectName is not provided, the task is added to the currently active project (set via setActiveProject). If projectName is provided, it overrides the active project for this command. An active project must be set or a project name provided. Optionally, a priority level and a due date can be included for the task."
Request Parameters:
taskDescription (string, required): "The textual description of the task to be performed."
projectName (string, optional): "The name of the project to which the task will be added. Defaults to the active project if not specified."
priority (integer, optional): "An optional numerical priority for the task. Defaults to no priority."
dueDate (string, optional): "An optional due date for the task (YYYY-MM-DD). Defaults to no due date."
Response (string):
Success: "Task added to '{projectName}' (ID: {task_id}): [ ] {taskDescription} (Priority: {P}, Due: {D})."
Error: "Error: Task description cannot be empty." or "Error: No project specified and no active project set..." or "Error: Project '{projectName}' not found." or "Error: Could not add task..."
4. listTasks
Description (for LLM): "Lists tasks. If projectName is not provided, lists tasks for the currently active project. If projectName is provided, it overrides the active project. An active project must be set or a project name provided. Tasks can be optionally filtered by their status (e.g., 'open', 'completed', or 'all'). Defaults to 'open' tasks if no filter is provided."

#### Request Parameters
- **projectName** (string, optional): "The name of the project whose tasks are to be listed. Defaults to the active project."
- **statusFilter** (string, optional): "Filter tasks by status: 'open', 'completed', or 'all'. Defaults to 'open'.

#### Response (string)
**Success:** A multi-line string. Each line follows the format:
`[marker] (ID: {id}) {description} (Priority: {P}, Due: {D}, Completed: {C})`

Example:
```
[ ] (ID: 1) Implement feature X (Priority: 1, Due: 2024-12-01)
[x] (ID: 2) Fix bug Y (Completed: 2024-11-15)
```

**No Tasks:** `"No {statusFilter} tasks found for project '{projectName}'."`

**Error:** One of:
- `"Error: Invalid status filter..."`
- `"Error: No project specified and no active project set..."`
- `"Error: Project '{projectName}' not found."`

### 5. markTaskComplete

#### Description (for LLM)
"Marks a specific task as completed. If projectName is not provided, operates on the currently active project. If projectName is provided, it overrides the active project. An active project must be set or a project name provided. The task is identified either by its unique numerical ID or by a unique portion of its description."

#### Request Parameters
- **taskIdOrDescription** (string, required): "The numerical ID of the task, or a unique identifying part of its description."
- **projectName** (string, optional): "The name of the project containing the task. Defaults to the active project."

#### Response (string)
**Success:** `"Task '(ID: {id}) {description}' in '{projectName}' marked as complete."`

**Info:** `"Info: Task '(ID: {id}) {description}' in '{projectName}' is already marked as complete."`

**Error:** One of:
- `"Error: Task identifier cannot be empty."`
- `"Error: No project specified..."`
- `"Error: Project '{projectName}' not found."`
- `"Error: Task '{taskIdOrDescription}' not found..."`
- `"Error: Could not mark task..."`

### 6. removeTask

#### Description (for LLM)
"Removes a specific task. If projectName is not provided, operates on the currently active project. If projectName is provided, it overrides the active project. An active project must be set or a project name provided. The task is identified either by its unique numerical ID or by a unique portion of its description."

#### Request Parameters
- **taskIdOrDescription** (string, required): "The numerical ID of the task, or a unique identifying part of its description."
- **projectName** (string, optional): "The name of the project from which the task will be removed. Defaults to the active project."

#### Response (string)
**Success:** `"Task '(ID: {id}) {description}' removed from '{projectName}'."`

**Error:** One of:
- `"Error: Task identifier cannot be empty."`
- `"Error: No project specified..."`
- `"Error: Project '{projectName}' not found."`
- `"Error: Task '{taskIdOrDescription}' not found..."`
- `"Error: Could not remove task..."`
