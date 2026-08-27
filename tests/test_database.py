import pytest
from voyage.database import create_task, database
from voyage.domain import Task
import sqlite3
import datetime

# Create a temporary SQLite database for testing
test_db = "test_voyage.db"

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup: Create the test database and tables
    conn = sqlite3.connect(test_db)
    csr = conn.cursor()
    csr.execute("PRAGMA foreign_keys = ON")
    
    csr.execute(
        """
CREATE TABLE IF NOT EXISTS goals(
id INTEGER PRIMARY KEY , 
title TEXT NOT NULL,
deadline TEXT ,
started_at TEXT NOT NULL
)
"""
    )
    
    csr.execute(
        """
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY , 
title TEXT NOT NULL, 
status TEXT NOT NULL, 
created_at TEXT NOT NULL,
completed_at TEXT  ,
goal_id INTEGER ,
FOREIGN KEY (goal_id) REFERENCES goals(id))
"""
    )
    
    conn.commit()
    conn.close()

    yield

    # Teardown: Remove the test database
    import os
    os.remove(test_db)

def test_create_task():
    # Create a task
    task = Task(
        id=1,
        title="Test Task",
        status="pending",
        created_at=datetime.datetime.now(),
        completed_at=None,
        goal_id=1
    )

    # Call the create_task function
    task_id = create_task(task)

    # Verify that the task is inserted into the tasks table
    conn = sqlite3.connect(test_db)
    csr = conn.cursor()
    csr.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    result = csr.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == task_id
    assert result[1] == task.title
    assert result[2] == task.status
    assert result[3] == task.created_at.isoformat()
    assert result[4] is None  # completed_at should be NULL

def test_create_task_with_completed_at():
    # Create a task with completed_at set
    task = Task(
        id=1,
        title="Test Task",
        status="completed",
        created_at=datetime.datetime.now(),
        completed_at=datetime.datetime.now(),
        goal_id=1
    )

    # Call the create_task function
    task_id = create_task(task)

    # Verify that the task is inserted into the tasks table
    conn = sqlite3.connect(test_db)
    csr = conn.cursor()
    csr.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    result = csr.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == task_id
    assert result[1] == task.title
    assert result[2] == task.status
    assert result[3] == task.created_at.isoformat()
    assert result[4] == task.completed_at.isoformat()  # completed_at should be stored as ISO format
