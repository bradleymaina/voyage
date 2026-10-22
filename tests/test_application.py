from datetime import datetime
from voyage.application import board_task, dock_task, stow_book, log_book
from voyage.database import init_db, get_task,update_task, add_book
from voyage.domain import Book
import pytest



def test_board_task_with_no_goal(tmp_path):
    db_path = tmp_path  / "test.db"
    con = init_db(db_path)
    cur = con.cursor()

    
    task = board_task(con , "Fix hwcheck battery error")
    created_at = task.created_at

    assert task.id is not None
    assert task.title == "Fix hwcheck battery error"
    assert task.status == "boarded"
    assert task.completed_at is None
    assert task.goal_id is None


    cur.execute(
        """
        SELECT title, status, created_at, completed_at, goal_id
        FROM tasks
        WHERE id = ?
        """,
        (task.id,),
    )

    saved_task = cur.fetchone()

    assert saved_task is not None
    assert saved_task == ("Fix hwcheck battery error", "boarded", created_at.isoformat(), None , None)


def test_board_task_with_goal(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(db_path)
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO goals (title, deadline, started_at) VALUES (?, ?, ? )
        """, ("Test goal", datetime.now().isoformat(), datetime.now().isoformat()))
    goal_id = cur.lastrowid
    con.commit()

    task = board_task(con, "Fix hwcheck battery error", goal_id)
    created_at = task.created_at

    assert task.id is not None
    assert task.title == "Fix hwcheck battery error"
    assert task.status == "boarded"
    assert task.completed_at is  None
    assert task.goal_id  is not  None

    cur.execute(
        """
        SELECT title , status, created_at, completed_at , goal_id
        FROM tasks
        WHERE id = ? 
        """,
        (task.id,),
    )

    saved_task = cur.fetchone()

    assert saved_task is not None
    assert saved_task == ("Fix hwcheck battery error", "boarded", created_at.isoformat(), None, goal_id)


def test_tasks_have_unique_id(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(db_path)
    cur = con.cursor()

    task = board_task(con, "test task")
    task_1 = board_task(con, "test task2")
    

    assert task.id  != task_1.id

def test_dock_task_docks_task_and_saves_it(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))

    task = board_task(con, "test task")
    returned_task = dock_task(con, task.id)
    saved_task = get_task(con, task.id)

    assert saved_task.completed_at is not None
    assert saved_task.status == "docked"
    assert saved_task.completed_at  == returned_task.completed_at
    con.close()
 
def test_dock_task_raises_when_task_not_found(tmp_path):
    db_path = tmp_path  / "test.db"
    con = init_db(str(db_path))

    with pytest.raises(ValueError, match="not found"):
        dock_task(con, 500)

    con.close()

def test_dock_task_raises_for_already_docked_task(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))

    task = board_task(con, "test task")
    returned_task = dock_task(con, task.id)
    first_completed_at = returned_task.completed_at


    with pytest.raises(ValueError, match="docked"):
       dock_task(con, task.id)

    saved_task = get_task(con, task.id)

    assert first_completed_at == saved_task.completed_at

    con.close()
    
def test_dock_task_raises_for_a_marooned_task(tmp_path):
    db_path = tmp_path  / "test.db"
    con = init_db(str(db_path))

    returned_task = board_task(con, "test task")
    returned_task.maroon()
    update_task(con, returned_task)
    con.commit()

    with pytest.raises(ValueError, match="marooned"):
        dock_task(con, returned_task.id)

    saved_task = get_task(con, returned_task.id)

    assert saved_task.completed_at is None
    assert saved_task.status == "marooned"

    con.close()

def test_stow_book_adds_book_and_saves_to_database(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))
    cur = con.cursor()

    book = stow_book(con, "test book", "John Doe", 500)
    started_at = book.started_at

    assert book.id is not None
    assert book.title == "test book"
    assert book.author == "John Doe"
    assert book.total_pages == 500
    assert book.current_page == 0
    assert book.updated_at is None


    cur.execute(
        """
        SELECT title , author, total_pages, current_page,  started_at, updated_at
        FROM books
        WHERE id = ?
        """,
        (book.id,),
    )

    saved_book = cur.fetchone()

    assert saved_book is not None
    assert saved_book == ("test book", "John Doe", 500, 0, started_at.isoformat(), None)

    con.close()

    #TODO:  test does not prove con.commit runs

def test_log_book_raises_when_book_is_not_in_database(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))


    with pytest.raises(ValueError, match="does not exist"):
        log_book(con, 999, 54)

def test_log_book_updates_page_and_updated_at(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))

    now = datetime.now()

    book = Book(
        id = None, 
        title = "test book",
        author = "John Doe",
        total_pages = 500,
        current_page = 5, 
        started_at = now,
        updated_at = None
    )

    book_id = add_book(con, book)
    updated_book = log_book(con, book_id, 64)

    assert updated_book.current_page == 64
    assert updated_book.updated_at is not None 

def test_log_book_raises_for_invalid_page(tmp_path):
    db_path = tmp_path / "test.db"
    con = init_db(str(db_path))

    now = datetime.now()

    book = Book(
        id = None,
        title = "test book",
        author = "John Doe",
        total_pages = 500,
        current_page = 30, 
        started_at  = now, 
        updated_at = None
    )

    book_id = add_book(con, book)

    with pytest.raises(ValueError , match="Invalid"):
        log_book(con, book_id, 800)

