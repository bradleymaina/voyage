import sqlite3
from voyage.domain import Task, Book, Goal

#database
database = "voyage.db"

db = sqlite3.connect(database)

db.execute("PRAGMA foreign_keys = ON")

csr = db.cursor()

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

csr.execute(
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
    task.created_at,
    task.completed_at,
    task.goal_id

)
    )

db.commit()
db.close()



