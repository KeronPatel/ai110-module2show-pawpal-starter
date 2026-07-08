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