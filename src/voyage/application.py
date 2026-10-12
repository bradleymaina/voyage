import sqlite3
from voyage.domain import Task
from voyage.database import create_task , get_task, update_task
from datetime import datetime

def board_task(con: sqlite3.Connection, title: str , goal_id: int | None =  None) -> Task:
    """Add a new task"""
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


def dock_task(con: sqlite3.Connection, task_id: int):
    """Complete a task """
    fetched_task = get_task(con, task_id)

    if fetched_task is None:
        raise ValueError(f" Task {task_id} was not found!")

    if fetched_task.status == "docked":
        raise ValueError("Task has already been docked")
       

    if fetched_task.status == "marooned":
        raise ValueError("A marooned task cannot be docked!")
        

    fetched_task.dock()
    update_task(con, fetched_task)
    con.commit()

    return fetched_task
