from datetime import datetime
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    status: str
    created_at: datetime
    completed_at: datetime | None

@dataclass
class Book:
    title: str
    author: str
    total_pages: int
    current_page: int
    started_at: datetime
    completed_at: datetime | None


    def get_progress(self) -> float:
        """get book progress"""
        if self.total_pages != 0:
            return self.current_page / self.total_pages * 100


@dataclass
class Goal:
    title: str
    stages: list
    deadline: datetime
    started_at: datetime | None
