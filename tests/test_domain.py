import pytest
from voyage.domain import Task, Book, Goal
from datetime import datetime

# Fixtures for common setup
@pytest.fixture
def task():
    return Task(
        id=1,
        title="Complete project",
        status="pending",
        created_at=datetime.now(),
        goal_id=None
    )

@pytest.fixture
def book():
    return Book(
        title="Python Programming",
        author="John Doe",
        total_pages=300,
        current_page=50,
        started_at=datetime.now()
    )

@pytest.fixture
def goal():
    return Goal(
        title="Read a book",
        deadline=None,
        started_at=datetime.now()
    )

# Test cases for Task class
def test_task_dock(task):
    # Given
    task.status = "pending"
    
    # When
    task.dock()
    
    # Then
    assert task.status == "complete"
    assert task.completed_at is not None

def test_task_maroon(task):
    # Given
    task.status = "pending"
    
    # When
    task.maroon()
    
    # Then
    assert task.status == "maroon"

# Test cases for Book class
def test_book_update_page(book):
    # Given
    new_page = 100
    
    # When
    book.update_page(new_page)
    
    # Then
    assert book.current_page == new_page
    assert book.updated_at is not None

def test_book_update_page_invalid_page(book):
    # Given
    invalid_page = -1
    
    # When & Then
    with pytest.raises(ValueError) as exc_info:
        book.update_page(invalid_page)
    
    assert str(exc_info.value) == "Invalid Page!"

def test_book_get_progress(book):
    # Given
    progress = book.get_progress()
    
    # Then
    assert progress == (book.current_page / book.total_pages) * 100

def test_book_is_complete(book):
    # Given
    completed_book = Book(
        title="Python Programming",
        author="John Doe",
        total_pages=300,
        current_page=300,
        started_at=datetime.now()
    )
    
    # When
    is_complete = completed_book.is_complete()
    
    # Then
    assert is_complete

# Test cases for Goal class
def test_goal_get_progress(goal):
    # Given
    tasks = [
        Task(
            id=1,
            title="Task 1",
            status="complete",
            created_at=datetime.now(),
            goal_id=None
        ),
        Task(
            id=2,
            title="Task 2",
            status="pending",
            created_at=datetime.now(),
            goal_id=None
        )
    ]
    
    # When
    progress = goal.get_progress(tasks)
    
    # Then
    assert progress == (1 / len(tasks)) * 100

def test_goal_get_progress_no_tasks(goal):
    # Given
    tasks = []
    
    # When
    progress = goal.get_progress(tasks)
    
    # Then
    assert progress == 0.0
