from datetime import datetime
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    status: str
    created_at: datetime
    completed_at: datetime | None = None

    def dock(self):
        self.status = "complete"
        self.completed_at = datetime.now()

    def maroon(self):
        self.status = "maroon"

@dataclass
class Book:
    title: str
    author: str
    total_pages: int
    current_page: int
    started_at: datetime
    updated_at: datetime | None

    def  update_page(self, page: int):
        if page < 0 or page > self.total_pages:
            raise ValueError("Invalid Page!")

        self.current_page = page
        self.updated_at = datetime.now()

         
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
