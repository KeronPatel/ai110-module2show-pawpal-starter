from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta

@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str               # format "HH:MM"
    duration: int           # minutes
    priority: str           # "low", "medium", "high"
    frequency: str          # "once", "daily", "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)
    pet_ref: Optional[object] = field(default=None, repr=False)

    def mark_complete(self):
        """Mark task done and auto-schedule next occurrence if recurring."""
        self.completed = True
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
            new_task = Task(
                description=self.description,
                time=self.time,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
                completed=False,
                due_date=next_date,
                pet_ref=self.pet_ref,
            )
            if self.pet_ref is not None:
                self.pet_ref.add_task(new_task)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
            new_task = Task(
                description=self.description,
                time=self.time,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
                completed=False,
                due_date=next_date,
                pet_ref=self.pet_ref,
            )
            if self.pet_ref is not None:
                self.pet_ref.add_task(new_task)


class Pet:
    """Stores pet details and a list of care tasks."""

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a task to this pet and link the task back to this pet."""
        task.pet_ref = self
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks


class Owner:
    """Manages an owner's profile and their collection of pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted chronologically by HH:MM time string."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return only tasks matching the given completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to a specific pet by name."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def detect_conflicts(self) -> List[str]:
        """Find tasks scheduled at the same time and return warning messages."""
        all_tasks = self.owner.get_all_tasks()
        time_map = {}
        for task in all_tasks:
            if task.time not in time_map:
                time_map[task.time] = []
            time_map[task.time].append(task.description)
        warnings = []
        for time, descriptions in time_map.items():
            if len(descriptions) > 1:
                joined = " and ".join(descriptions)
                warnings.append(f"Conflict at {time}: {joined}")
        return warnings