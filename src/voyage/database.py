import sqlite3
from voyage.domain import Task, Book, Goal

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
    return cur.lastrowid()