import sqlite3
from voyage.domain import Task, Book, Goal
from datetime import datetime

def init_db(db: str) -> sqlite3.Connection:
    con = sqlite3.connect(db)

    con.execute("PRAGMA foreign_keys=ON")

    cur = con.cursor() 

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS goals(
    id INTEGER PRIMARY KEY , 
    title TEXT NOT NULL,
    deadline TEXT ,
    started_at TEXT NOT NULL
    )
    """
    )

    cur.execute(
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

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY , 
    title TEXT NOT NULL, 
    author TEXT NOT NULL, 
    total_pages INTEGER NOT NULL, 
    current_page INTEGER NOT NULL,
    started_at TEXT NOT NULL, 
    updated_at TEXT
    )
    """
    )
    con.commit()
    
    return con 

def  create_task(con: sqlite3.Connection,  task: Task):
    cur = con.cursor()
    cur.execute(
        """
INSERT INTO tasks(
title,
status,
created_at,
completed_at,
goal_id
)
VALUES (?, ?, ?, ?, ?)
""",
(
    task.title, 
    task.status,
    task.created_at.isoformat(),
    task.completed_at.isoformat() if task.completed_at else None,
    task.goal_id

)
    )

    return cur.lastrowid

def get_task(con: sqlite3.Connection, task_id: int) -> Task | None:
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM tasks
        WHERE id=?
        """,
        (task_id,)
    )

    selected_task = cur.fetchone()

    if selected_task is None :
        return None
    else:

        task = Task(
            id = selected_task[0],
            title = selected_task[1],
            status = selected_task[2],
            created_at = datetime.fromisoformat(selected_task[3]),
            completed_at = datetime.fromisoformat(selected_task[4]) if selected_task[4] else None,
            goal_id = selected_task[5] 
        )
    return task

def update_task(con: sqlite3.Connection, task: Task):
    cur = con.cursor()
    cur.execute(
        """
        UPDATE tasks
        SET status = ?,
            completed_at = ?
        WHERE
          id = ? ;
        """, 
        (task.status, task.completed_at.isoformat(), task.id) #TODO: Use SET to avoid writing  another function for renaming task
    )


def add_book(con: sqlite3.Connection, book: Book):
    cur = con.cursor()
    cur.execute(
        """
INSERT INTO books(
title,
author,
total_pages,
current_page,
started_at,
updated_at
)
VALUES (?, ?, ?, ?, ?, ?)
""",
(
    book.title,
    book.author,
    book.total_pages,
    book.current_page,
    book.started_at.isoformat(),
    book.updated_at.isoformat()
)
    )
    return cur.lastrowid


def add_goal(con: sqlite3.Connection, goal: Goal):
    cur = con.cursor()
    cur.execute(
        """
INSERT INTO goals(
title, 
deadline,
started_at
)
VALUES (?,?,?)
""",
(
    goal.title, 
    goal.deadline.isoformat() if goal.deadline else None,
    goal.started_at.isoformat()
)
    )
    return cur.lastrowid