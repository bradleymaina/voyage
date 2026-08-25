import sqlite3

#database
database = "voyage.db"

db = sqlite3.connect(database)
csr = db.cursor()


csr.execute(
    """
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT, 
title TEXT NOT NULL, 
status TEXT NOT NULL, 
created_at TEXT NOT NULL,
completed_at TEXT  ,
goal_id INTEGER )
"""
)

csr.execute(
    """
CREATE TABLE IF NOT EXISTS books(
book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
title TEXT NOT NULL, 
author TEXT NOT NULL, 
total_pages INTEGER NOT NULL, 
current_page INTEGER NOT NULL,
started_at TEXT NOT NULL, 
updated_at TEXT
)
"""
)

