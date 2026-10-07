import pytest
from datetime import datetime
from voyage.application import board_task
from voyage.database import init_db


def test_board_task_with_no_goal(tmp_path):
    db_path = tmp_path  / "test.db"
    con = init_db(db_path)
    cur = con.cursor()

    
    task = board_task(con , "Fix hwcheck battery error")
    created_at = task.created_at

    assert task.id is not None
    assert task.title == "Fix hwcheck battery error"
    assert task.status == "boarded"
    assert task.completed_at is None
    assert task.goal_id is None


    cur.execute(
        """
        SELECT title, status, created_at, completed_at, goal_id
        FROM tasks
        WHERE id = ?
        """,
        (task.id,),
    )

    saved_task = cur.fetchone()

    assert saved_task is not None
    assert saved_task == ("Fix hwcheck battery error", "boarded", created_at.isoformat(), None , None)


def test_board_task_with_goal(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(db_path)
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO goals (title, deadline, started_at) VALUES (?, ?, ? )
        """, ("Test goal", datetime.now().isoformat(), datetime.now().isoformat()))
    goal_id = cur.lastrowid
    con.commit()

    task = board_task(con, "Fix hwcheck battery error", goal_id)
    created_at = task.created_at

    assert task.id is not None
    assert task.title == "Fix hwcheck battery error"
    assert task.status == "boarded"
    assert task.completed_at is  None
    assert task.goal_id  is not  None

    cur.execute(
        """
        SELECT title , status, created_at, completed_at , goal_id
        FROM tasks
        WHERE id = ? 
        """,
        (task.id,),
    )

    saved_task = cur.fetchone()

    assert saved_task is not None
    assert saved_task == ("Fix hwcheck battery error", "boarded", created_at.isoformat(), None, goal_id)


def test_tasks_have_unique_id(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(db_path)
    cur = con.cursor()

    task = board_task(con, "test task")
    task_1 = board_task(con, "test task2")
    

    assert task.id  != task_1.id

