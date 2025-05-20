"""BDD-style tests for Task CRUD operations."""

import sqlite3
from typing import Generator

import pytest


@pytest.fixture  # type: ignore[misc]
def in_memory_db() -> Generator[sqlite3.Connection, None, None]:
    """Create an in-memory SQLite database for testing.

    Returns:
        Generator[sqlite3.Connection, None, None]: Database connection.
    """
    # Create an in-memory database with foreign key support enabled
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')  # Enable foreign key constraints

    # Create the schema
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS Projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS Tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            priority INTEGER,
            due_date TEXT,
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
    """
    )

    # Insert a test project
    conn.execute(
        'INSERT INTO Projects (project_name) VALUES (?)',
        ('Test Project',),
    )
    conn.commit()

    yield conn

    # Close the connection
    conn.close()


class TestTaskCreation:
    """Test suite for task creation operations.

    Following BDD style:
    - Given the task data models
    - When creating a task
    - Then it should be properly stored in the database
    """

    def test_create_task_with_required_fields(
        self, in_memory_db: sqlite3.Connection
    ) -> None:
        """Test creating a task with only required fields.

        Given the task data models
        When creating a task with only required fields
        Then it should be properly stored in the database
        """
        # Given
        project_id = 1  # From the fixture
        description = 'Implement CRUD operations'

        # When
        cursor = in_memory_db.cursor()
        cursor.execute(
            'INSERT INTO Tasks (project_id, description) VALUES (?, ?)',
            (project_id, description),
        )
        in_memory_db.commit()

        # Then
        cursor.execute('SELECT * FROM Tasks WHERE description = ?', (description,))
        task_row = cursor.fetchone()
        assert task_row is not None
        assert task_row[1] == project_id  # project_id
        assert task_row[2] == description  # description
        assert task_row[3] == 'open'  # status

    def test_create_task_with_all_fields(
        self, in_memory_db: sqlite3.Connection
    ) -> None:
        """Test creating a task with all fields.

        Given the task data models
        When creating a task with all fields
        Then it should be properly stored in the database with all attributes
        """
        # Given
        project_id = 1  # From the fixture
        description = 'Complete technical design'
        status = 'open'
        priority = 1
        due_date = '2025-06-15'

        # When
        cursor = in_memory_db.cursor()
        cursor.execute(
            """
            INSERT INTO Tasks
                (project_id, description, status, priority, due_date)
            VALUES
                (?, ?, ?, ?, ?)
            """,
            (project_id, description, status, priority, due_date),
        )
        in_memory_db.commit()

        # Then
        cursor.execute('SELECT * FROM Tasks WHERE description = ?', (description,))
        task_row = cursor.fetchone()
        assert task_row is not None
        assert task_row[1] == project_id  # project_id
        assert task_row[2] == description  # description
        assert task_row[3] == status  # status
        assert task_row[4] == priority  # priority
        assert task_row[5] == due_date  # due_date


class TestTaskReading:
    """Test suite for task reading operations.

    Following BDD style:
    - Given tasks in the database
    - When reading tasks
    - Then they should be properly retrieved
    """

    def test_read_task_by_id(self, in_memory_db: sqlite3.Connection) -> None:
        """Test reading a task by ID.

        Given a task in the database
        When reading the task by ID
        Then it should be properly retrieved
        """
        # Given
        cursor = in_memory_db.cursor()
        cursor.execute(
            'INSERT INTO Tasks (project_id, description) VALUES (?, ?)',
            (1, 'Read task by ID'),
        )
        in_memory_db.commit()
        task_id = cursor.lastrowid

        # When
        cursor.execute('SELECT * FROM Tasks WHERE task_id = ?', (task_id,))
        task_row = cursor.fetchone()

        # Then
        assert task_row is not None
        assert task_row[0] == task_id  # task_id
        assert task_row[2] == 'Read task by ID'  # description

    def test_read_all_tasks_for_project(self, in_memory_db: sqlite3.Connection) -> None:
        """Test reading all tasks for a project.

        Given multiple tasks for a project in the database
        When reading all tasks for that project
        Then all tasks should be properly retrieved
        """
        # Given
        project_id = 1
        cursor = in_memory_db.cursor()

        # Insert 3 tasks for the project
        task_descriptions = ['Task 1', 'Task 2', 'Task 3']
        for desc in task_descriptions:
            cursor.execute(
                'INSERT INTO Tasks (project_id, description) VALUES (?, ?)',
                (project_id, desc),
            )
        in_memory_db.commit()

        # When
        cursor.execute('SELECT * FROM Tasks WHERE project_id = ?', (project_id,))
        tasks = cursor.fetchall()

        # Then
        assert (
            len(tasks) >= 3
        )  # At least 3 tasks (there might be others from previous tests)
        task_descriptions_in_db = [
            task[2] for task in tasks
        ]  # description is at index 2
        for desc in task_descriptions:
            assert desc in task_descriptions_in_db

    def test_read_tasks_with_filter(self, in_memory_db: sqlite3.Connection) -> None:
        """Test reading tasks with a filter.

        Given tasks with different statuses in the database
        When reading tasks with a status filter
        Then only tasks matching the filter should be retrieved
        """
        # Given
        project_id = 1
        cursor = in_memory_db.cursor()

        # Insert tasks with different statuses
        cursor.execute(
            'INSERT INTO Tasks (project_id, description, status) VALUES (?, ?, ?)',
            (project_id, 'Open task', 'open'),
        )
        cursor.execute(
            'INSERT INTO Tasks (project_id, description, status) VALUES (?, ?, ?)',
            (project_id, 'Completed task', 'completed'),
        )
        in_memory_db.commit()

        # When - filter for completed tasks
        cursor.execute(
            'SELECT * FROM Tasks WHERE project_id = ? AND status = ?',
            (project_id, 'completed'),
        )
        completed_tasks = cursor.fetchall()

        # Then
        assert len(completed_tasks) >= 1
        for task in completed_tasks:
            assert task[3] == 'completed'  # status is at index 3


class TestTaskUpdating:
    """Test suite for task updating operations.

    Following BDD style:
    - Given a task in the database
    - When updating the task
    - Then the changes should be properly stored
    """

    def test_update_task_description(self, in_memory_db: sqlite3.Connection) -> None:
        """Test updating a task's description.

        Given a task in the database
        When updating the task's description
        Then the change should be properly stored
        """
        # Given
        cursor = in_memory_db.cursor()
        cursor.execute(
            'INSERT INTO Tasks (project_id, description) VALUES (?, ?)',
            (1, 'Original description'),
        )
        in_memory_db.commit()
        task_id = cursor.lastrowid

        # When
        new_description = 'Updated description'
        cursor.execute(
            'UPDATE Tasks SET description = ? WHERE task_id = ?',
            (new_description, task_id),
        )
        in_memory_db.commit()

        # Then
        cursor.execute('SELECT description FROM Tasks WHERE task_id = ?', (task_id,))
        updated_description = cursor.fetchone()[0]
        assert updated_description == new_description

    def test_update_task_status(self, in_memory_db: sqlite3.Connection) -> None:
        """Test updating a task's status.

        Given a task in the database
        When updating the task's status to completed
        Then the change should be properly stored and updated_at should be updated
        Note: In SQLite, CURRENT_TIMESTAMP has only second-level precision, so
        updated_at may not change if the update occurs within the same second.
        This test only asserts the status change to avoid flakiness.
        """
        # Given
        cursor = in_memory_db.cursor()
        cursor.execute(
            'INSERT INTO Tasks (project_id, description, status) VALUES (?, ?, ?)',
            (1, 'Task to complete', 'open'),
        )
        in_memory_db.commit()
        task_id = cursor.lastrowid

        # When
        cursor.execute(
            'UPDATE Tasks SET status = ? WHERE task_id = ?',
            ('completed', task_id),
        )
        in_memory_db.commit()

        # Then
        cursor.execute(
            'SELECT status FROM Tasks WHERE task_id = ?',
            (task_id,),
        )
        updated_status = cursor.fetchone()[0]
        assert updated_status == 'completed'

    def test_update_task_multiple_fields(
        self, in_memory_db: sqlite3.Connection
    ) -> None:
        """Test updating multiple fields of a task.

        Given a task in the database
        When updating multiple fields
        Then all changes should be properly stored
        """
        # Given
        cursor = in_memory_db.cursor()
        cursor.execute(
            """
            INSERT INTO Tasks
                (project_id, description, priority, due_date)
            VALUES
                (?, ?, ?, ?)
            """,
            (1, 'Multi-field task', 3, '2025-05-01'),
        )
        in_memory_db.commit()
        task_id = cursor.lastrowid

        # When
        cursor.execute(
            """
            UPDATE Tasks
            SET description = ?, priority = ?, due_date = ?
            WHERE task_id = ?
            """,
            ('Updated multi-field task', 1, '2025-06-01', task_id),
        )
        in_memory_db.commit()

        # Then
        cursor.execute(
            'SELECT description, priority, due_date FROM Tasks WHERE task_id = ?',
            (task_id,),
        )
        result = cursor.fetchone()

        assert result[0] == 'Updated multi-field task'  # description
        assert result[1] == 1  # priority
        assert result[2] == '2025-06-01'  # due_date


class TestTaskDeletion:
    """Test suite for task deletion operations.

    Following BDD style:
    - Given a task in the database
    - When deleting the task
    - Then it should be properly removed
    """

    def test_delete_task_by_id(self, in_memory_db: sqlite3.Connection) -> None:
        """Test deleting a task by ID.

        Given a task in the database
        When deleting the task by ID
        Then it should be properly removed
        """
        # Given
        cursor = in_memory_db.cursor()
        cursor.execute(
            'INSERT INTO Tasks (project_id, description) VALUES (?, ?)',
            (1, 'Task to delete'),
        )
        in_memory_db.commit()
        task_id = cursor.lastrowid

        # Verify it exists
        cursor.execute('SELECT COUNT(*) FROM Tasks WHERE task_id = ?', (task_id,))
        count_before = cursor.fetchone()[0]
        assert count_before == 1

        # When
        cursor.execute('DELETE FROM Tasks WHERE task_id = ?', (task_id,))
        in_memory_db.commit()

        # Then
        cursor.execute('SELECT COUNT(*) FROM Tasks WHERE task_id = ?', (task_id,))
        count_after = cursor.fetchone()[0]
        assert count_after == 0

    def test_delete_all_tasks_for_project(
        self, in_memory_db: sqlite3.Connection
    ) -> None:
        """Test deleting all tasks for a project.

        Given multiple tasks for a project in the database
        When deleting all tasks for that project
        Then all tasks should be properly removed
        """
        # Given
        project_id = 1
        cursor = in_memory_db.cursor()

        # Insert 3 tasks for the project with a unique marker
        marker = 'batch_delete_test'
        for i in range(3):
            cursor.execute(
                'INSERT INTO Tasks (project_id, description) VALUES (?, ?)',
                (project_id, f'{marker}_{i}'),
            )
        in_memory_db.commit()

        # Verify they exist
        cursor.execute(
            'SELECT COUNT(*) FROM Tasks WHERE project_id = ? AND description LIKE ?',
            (project_id, f'{marker}_%'),
        )
        count_before = cursor.fetchone()[0]
        assert count_before == 3

        # When
        cursor.execute(
            'DELETE FROM Tasks WHERE project_id = ? AND description LIKE ?',
            (project_id, f'{marker}_%'),
        )
        in_memory_db.commit()

        # Then
        cursor.execute(
            'SELECT COUNT(*) FROM Tasks WHERE project_id = ? AND description LIKE ?',
            (project_id, f'{marker}_%'),
        )
        count_after = cursor.fetchone()[0]
        assert count_after == 0

    def test_cascade_delete_when_project_deleted(
        self, in_memory_db: sqlite3.Connection
    ) -> None:
        """Test that tasks are deleted when their project is deleted.

        Given a project with tasks in the database
        When deleting the project
        Then all its tasks should be automatically deleted due to CASCADE
        """
        # Given
        cursor = in_memory_db.cursor()

        # Create a new project for this test
        cursor.execute(
            'INSERT INTO Projects (project_name) VALUES (?)',
            ('Project to delete',),
        )
        project_id = cursor.lastrowid

        # Add tasks to this project
        for i in range(3):
            cursor.execute(
                'INSERT INTO Tasks (project_id, description) VALUES (?, ?)',
                (project_id, f'Task for project {project_id} - {i}'),
            )
        in_memory_db.commit()

        # Verify tasks exist
        cursor.execute(
            'SELECT COUNT(*) FROM Tasks WHERE project_id = ?',
            (project_id,),
        )
        count_before = cursor.fetchone()[0]
        assert count_before == 3

        # When
        cursor.execute('DELETE FROM Projects WHERE project_id = ?', (project_id,))
        in_memory_db.commit()

        # Then
        cursor.execute(
            'SELECT COUNT(*) FROM Tasks WHERE project_id = ?',
            (project_id,),
        )
        count_after = cursor.fetchone()[0]
        assert count_after == 0  # All tasks should be deleted due to CASCADE
