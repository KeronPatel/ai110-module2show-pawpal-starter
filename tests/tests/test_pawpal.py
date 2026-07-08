from pawpal_system import Task, Pet, Owner, Scheduler

def test_mark_complete_changes_status():
    """Task completion status should change to True after mark_complete."""
    task = Task("Walk", "08:00", 30, "high", "once")
    task.mark_complete()
    assert task.completed == True

def test_add_task_increases_count():
    """Adding a task to a pet should increase its task count by 1."""
    pet = Pet("Biscuit", "dog")
    pet.add_task(Task("Walk", "08:00", 30, "high", "once"))
    assert len(pet.get_tasks()) == 1

def test_sort_by_time():
    """Tasks should come back in chronological order."""
    owner = Owner("Jordan")
    pet = Pet("Biscuit", "dog")
    pet.add_task(Task("Evening walk", "17:00", 30, "medium", "daily"))
    pet.add_task(Task("Morning walk", "08:00", 30, "high", "daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    assert sorted_tasks[0].time == "08:00"
    assert sorted_tasks[1].time == "17:00"

# ── 3 new tests ────────────────────────────────────────────────────────────────

def test_conflict_detection():
    """Scheduler should flag two tasks scheduled at the same time."""
    owner = Owner("Jordan")
    pet = Pet("Biscuit", "dog")
    pet.add_task(Task("Morning walk", "09:00", 30, "high", "daily"))
    pet.add_task(Task("Medication",   "09:00",  5, "high", "daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0
    assert "09:00" in conflicts[0]

def test_recurring_daily_task():
    """Completing a daily task should auto-add a new incomplete task to the pet."""
    pet = Pet("Mochi", "cat")
    task = Task("Feeding", "08:00", 10, "high", "daily")
    pet.add_task(task)
    initial_count = len(pet.get_tasks())
    task.mark_complete()
    assert len(pet.get_tasks()) == initial_count + 1
    new_task = pet.get_tasks()[-1]
    assert new_task.completed == False
    assert new_task.description == "Feeding"

def test_filter_by_status():
    """filter_by_status(False) should return only incomplete tasks."""
    owner = Owner("Jordan")
    pet = Pet("Biscuit", "dog")
    done_task = Task("Morning walk", "08:00", 30, "high", "once")
    done_task.completed = True
    pending_task = Task("Feeding", "09:00", 10, "high", "once")
    pet.add_task(done_task)
    pet.add_task(pending_task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    incomplete = scheduler.filter_by_status(False)
    assert len(incomplete) == 1
    assert incomplete[0].description == "Feeding"