"""Test database module """

import pytest
from datetime import datetime
from voyage.database import init_db, create_task
from voyage.domain import Task

def test_init_db_creates_goal_table(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='goals'")
    result = cur.fetchone()
    assert result is not None

def test_init_db_creates_task_table(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type= 'table' AND name= 'tasks'")
    result = cur.fetchone()
    assert result is not None

def test_init_db_creates_book_table(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type= 'table' AND name= 'books'")
    result = cur.fetchone()
    assert result is not None

def test_create_task_returns_id_and_saves_to_database(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))
    cur = con.cursor()
    """Enter goal table to satisfy foreign key constraint"""
    cur.execute('''
    INSERT INTO goals (title, deadline, started_at) VALUES (?, ?, ?)
    ''', ("Test Goal", datetime.now().isoformat(), datetime.now().isoformat()))
    goal_id = cur.lastrowid
    con.commit()

    now = datetime.now()
    task = Task(
        id= None,
        title= "Eddie",
        status= "incomplete",
        created_at= now,
        completed_at= None,
        goal_id = 1
    )

    task_id = create_task(con, task)
 
    assert isinstance(task_id, int)
    assert task_id > 0

    cur.execute(
        """
        SELECT title, status, created_at, completed_at, goal_id
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )
    saved_task = cur.fetchone()

    assert saved_task is not None
    assert saved_task == ("Eddie", "incomplete", now.isoformat(), None, 1)

    con.close()

def test_create_task_accepts_empty_values_for_completed_at_and_goal_id(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))
    cur = con.cursor()

    now = datetime.now()
    task = Task(
        id = None,
        title = "test",
        status = "complete",
        created_at = now,
        completed_at = None,
        goal_id = None
    )

    task_id = create_task(con, task)

    cur.execute(
        """
        SELECT title , status, created_at, completed_at, goal_id
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )
    saved_task = cur.fetchone()

    assert saved_task is not None
    assert saved_task == ("test", "complete", now.isoformat(), None, None)


