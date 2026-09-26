"""Test database module """

import pytest
from datetime import datetime
from voyage.database import init_db, create_task, add_book, add_goal
from voyage.domain import Task, Book, Goal

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


def test_add_book_returns_id_and_saves_to_database_and_updated_at_accepts_null_values(tmp_path):
    db_path = tmp_path / "test.db"

    con = init_db(str(db_path))
    cur = con.cursor()

    now = datetime.now()

    book = Book(
        id = None,
        title = "Computer Architecture, A Quantative Approach",
        author = "John L. Hennessy",
        total_pages = 500,
        current_page = 30,
        started_at = now,
        updated_at = now
    )

    book_id = add_book(con, book)

    cur.execute(
        """
        SELECT title, author, total_pages, current_page, started_at, updated_at
        FROM books
        WHERE id = ?
        """,
        (book_id,),
    )
    saved_book = cur.fetchone()

    assert saved_book is not None
    assert saved_book == ("Computer Architecture, A Quantative Approach", "John L. Hennessy", 500, 30, now.isoformat(), now.isoformat())

def test_add_goal_returns_goal_id_and_saves_to_database(tmp_path):
    db_path = tmp_path / "test.db"

    con = init_db(str(db_path))
    cur = con.cursor()

    now = datetime.now()

    goal = Goal(
        id = None, 
        title = "Read about MVC architecture",
        deadline = now,
        started_at = now
    )

    goal_id = add_goal(con, goal)

    cur.execute(
        """
        SELECT title, deadline, started_at
        FROM goals
        WHERE id = ?
        """,
        (goal_id,),
    )
    saved_goal = cur.fetchone()

    assert saved_goal is not None
    assert saved_goal == ("Read about MVC architecture", now.isoformat(), now.isoformat())

def test_deadline_accepts_null_values(tmp_path):
    db_path = tmp_path / "test.db"

    con = init_db(str(db_path))
    cur = con.cursor()

    now = datetime.now()

    goal = Goal(
        id = None,
        title = "Read Allan Turing Paper",
        deadline = None,
        started_at = now
    )

    goal_id = add_goal(con,goal)

    cur.execute(
        """
        SELECT title, deadline, started_at
        FROM goals
        WHERE id = ?
        """,
        (goal_id,),
    )
    saved_goal = cur.fetchone()

    assert saved_goal is not None
    assert saved_goal == ("Read Allan Turing Paper", None, now.isoformat())