from dataclasses import dataclass, field
from typing import List
from datetime import date, timedelta

@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str          # format "HH:MM"
    duration: int      # minutes
    priority: str      # "low", "medium", "high"
    frequency: str     # "once", "daily", "weekly"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        pass

class Pet:
    """Stores pet details and a list of tasks."""
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a task to this pet's list."""
        pass

    def get_tasks(self):
        """Return all tasks for this pet."""
        pass

class Owner:
    """Manages multiple pets."""
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        pass

    def get_all_tasks(self):
        """Return all tasks across all pets."""
        pass

class Scheduler:
    """Retrieves, sorts, and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self):
        """Return all tasks sorted by time."""
        pass

    def filter_by_status(self, completed: bool):
        """Return tasks filtered by completion status."""
        pass

    def detect_conflicts(self):
        """Return list of conflicting task time pairs."""
        pass