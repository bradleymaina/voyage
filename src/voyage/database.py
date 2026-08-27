import sqlite3
from voyage.domain import Task, Book, Goal

def init_db(db: str):
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

    return con 

def  create_task(task: Task):
    csr.execute(
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

    return csr.lastrowid

db.commit()
db.close()



