from datetime import datetime
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    status: str
    created_at: datetime
    completed_at: datetime | None = None
    goal_id: int | None = None

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
        return self.current_page / self.total_pages * 100

    def is_complete(self) -> bool:
        return self.current_page == self.total_pages

@dataclass
class Goal:
    title: str
    deadline: datetime | None
    started_at: datetime 


    def get_progress(self, tasks: list[Task]) -> float:
        if not tasks:
            return 0.0

        completed_tasks = 0 

        for task in tasks: 
            if task.status == "complete": 
                completed_tasks += 1

        return completed_tasks / len(tasks) * 100
    
