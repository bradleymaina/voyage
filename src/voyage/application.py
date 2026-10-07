import sqlite3
from voyage.domain import Task
from voyage.database import create_task 
from datetime import datetime

def board_task(con: sqlite3.Connection, title: str , goal_id: int | None =  None) -> Task:
    now = datetime.now()
    task = Task(
        id = None, 
        title = title, 
        status = "boarded", 
        created_at = now,
        completed_at = None,
        goal_id = goal_id
    )
    task.id = create_task(con, task) 
    con.commit()

    return task