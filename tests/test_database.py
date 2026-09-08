"""Test database module """

import pytest
from voyage.database import init_db

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
    