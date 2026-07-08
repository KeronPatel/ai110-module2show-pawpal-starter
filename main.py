from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner("Jordan")
dog = Pet("Biscuit", "dog")
cat = Pet("Mochi", "cat")

dog.add_task(Task("Morning walk", "08:00", 30, "high", "daily"))
dog.add_task(Task("Feeding", "09:00", 10, "high", "daily"))
dog.add_task(Task("Evening walk", "17:00", 30, "medium", "daily"))
cat.add_task(Task("Feeding", "08:00", 5, "high", "daily"))
cat.add_task(Task("Medication", "09:00", 5, "high", "daily"))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)
sorted_tasks = scheduler.sort_by_time()

print("=== Today's Schedule ===")
for task in sorted_tasks:
    status = "✓" if task.completed else "○"
    print(f"  {task.time} [{status}] {task.description} ({task.duration} min) [{task.priority}]")

conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n⚠ Conflicts detected:")
    for c in conflicts:
        print(f"  {c}")
else:
    print("\n✓ No conflicts found.")