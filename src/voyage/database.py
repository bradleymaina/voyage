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

