"""Task and Project data models for Copilot Task Manager MCP."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """Represents a project in the task manager."""

    project_id: Optional[int] = None
    project_name: str = ''
    created_at: Optional[datetime] = None


@dataclass
class Task:
    """Represents a task in the task manager."""

    task_id: Optional[int] = None
    project_id: int = 0
    description: str = ''
    status: str = 'open'  # 'open' or 'completed'
    priority: Optional[int] = None
    due_date: Optional[str] = None  # ISO8601: YYYY-MM-DD
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def mark_complete(self) -> None:
        """Mark the task as completed and update the timestamp."""
        self.status = 'completed'
        self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """Return True if the task is overdue and not completed."""
        if self.due_date:
            try:
                due = datetime.strptime(self.due_date, '%Y-%m-%d')
                return due < datetime.now() and self.status != 'completed'
            except ValueError:
                return False
        return False
