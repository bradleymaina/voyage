import sqlite3
from voyage.domain import Task, Book, Goal
from voyage.database import create_task , get_task, update_task, add_book, get_book, update_book, add_goal
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

def stow_book(con : sqlite3.Connection, title: str, author: str, total_pages: int ):
    """Add a new book"""
    now = datetime.now()

    book = Book(
        id = None,
        title = title,
        author = author,
        total_pages = total_pages,
        current_page = 0, 
        started_at = now, 
        updated_at = None,
    )

    if book.total_pages < 0:
        raise ValueError("Book cannot have negative pages!")

    book.id = add_book(con, book)
    con.commit()

    return book

def log_book(con: sqlite3.Connection, book_id: int, current_page: int):
    """Update a book """
    fetched_book = get_book(con, book_id)

    if fetched_book is None:
        raise ValueError(f"Book {book_id} does not exist!")
    

    fetched_book.update_page(current_page)
    update_book(con, fetched_book)
    con.commit()

    return fetched_book

def set_course(con: sqlite3.Connection, title: str) -> Goal:
    """Add a new goal"""
    now = datetime.now()
    goal = Goal(
        id = None,
        title = title,
        deadline = None,
        started_at = now
    )

    goal.id = add_goal(con, goal)
    con.commit()

    return goal
