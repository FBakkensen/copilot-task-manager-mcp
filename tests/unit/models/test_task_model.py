"""BDD-style tests for Task and Project data models."""

from datetime import datetime, timedelta

from src.copilot_task_manager.models import Project, Task


class TestTaskModel:
    """BDD-style tests for the Task data model."""

    def test_create_task_with_required_attributes(self) -> None:
        """Test creating a Task with required attributes."""
        # Given requirements for task management
        # When a Task is created with required attributes
        task = Task(project_id=1, description='Write BDD tests')
        # Then it should represent a task with appropriate attributes
        assert task.project_id == 1
        assert task.description == 'Write BDD tests'
        assert task.status == 'open'
        assert task.priority is None
        assert task.due_date is None
        assert task.created_at is None
        assert task.updated_at is None

    def test_task_mark_complete(self) -> None:
        """Test marking a task as complete."""
        # Given an open task
        task = Task(project_id=1, description='Finish docs')
        # When mark_complete is called
        task.mark_complete()
        # Then the status should be 'completed' and updated_at set
        assert task.status == 'completed'
        assert isinstance(task.updated_at, datetime)

    def test_task_is_overdue(self) -> None:
        """Test is_overdue returns True for overdue tasks."""
        # Given a task with a past due date
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        task = Task(project_id=1, description='Overdue task', due_date=yesterday)
        # When checking if overdue
        # Then is_overdue should be True
        assert task.is_overdue() is True

    def test_task_is_not_overdue_if_completed(self) -> None:
        """Test is_overdue returns False for completed tasks."""
        # Given a completed task with a past due date
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        task = Task(
            project_id=1,
            description='Done',
            due_date=yesterday,
            status='completed',
        )
        # When checking if overdue
        # Then is_overdue should be False
        assert task.is_overdue() is False

    def test_task_is_not_overdue_if_due_date_invalid(self) -> None:
        """Test is_overdue returns False for invalid due dates."""
        # Given a task with an invalid due date
        task = Task(
            project_id=1,
            description='Bad date',
            due_date='not-a-date',
        )
        # When checking if overdue
        # Then is_overdue should be False
        assert task.is_overdue() is False


class TestProjectModel:
    """BDD-style tests for the Project data model."""

    def test_create_project(self) -> None:
        """Test creating a Project with required attributes."""
        # Given requirements for project management
        # When a Project is created
        project = Project(project_id=1, project_name='Test Project')
        # Then it should represent a project with appropriate attributes
        assert project.project_id == 1
        assert project.project_name == 'Test Project'
        assert project.created_at is None
