# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    Three core actions a user should be able to perform:
    1. Add a pet with basic info (name, species)
    2. Schedule a care task for a pet (walk, feeding, medication, etc.)
    3. View today's tasks sorted by time

- What classes did you include, and what responsibilities did you assign to each?
    Classes chosen:
    - Task: holds what needs to happen, when, how long, and priority
    - Pet: stores pet details and owns a list of tasks
    - Owner: manages multiple pets and provides access to all tasks
    - Scheduler: the "brain" that sorts, filters, and checks for conflicts

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    After reviewing the initial skeleton with AI feedback, I made the following changes:

    1. Added a `pet_ref` field to the Task dataclass — the initial design did not give tasks a way to know which pet they belonged to. This was needed so that when mark_complete() creates a new recurring task, it can automatically add it to the correct pet without extra code in app.py.

    2. Added a `due_date` field to Task — the original skeleton only had a time string (HH:MM). Adding a date field was necessary to calculate the next occurrence for daily and weekly recurring tasks using timedelta.

    3. Added a `filter_by_pet(pet_name)` method to Scheduler — the original UML only had filter_by_status. This extra method makes it easier to show one pet's tasks at a time in the UI.

    These changes were identified after asking the AI to review the skeleton for missing relationships and potential logic bottlenecks.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
    - My scheduler considers three constraints: time (tasks are sorted by HH:MM so earlier tasks appear first), priority (low, medium, high labels are attached to every task so the owner can see what matters most), and frequency (once, daily, weekly determines whether a new task is auto-created after completion).
    - I decided time and priority mattered most because a pet owner's biggest pain point is knowing what to do and when. Frequency came second because recurring tasks like feeding and medication happen every day and should not require manual re-entry.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
    The most significant tradeoff in my Scheduler is how conflict detection works. My current implementation only flags tasks that share the exact same start time string (e.g., two tasks both at "09:00"). It does not account for overlapping durations — for example, a 30-minute task starting at 08:00 and a 15-minute task starting at 08:20 would overlap in real life, but my scheduler would not catch that conflict because their start times are different strings.

    I made this tradeoff intentionally because exact-time matching is simple, readable, and easy to test. Implementing true overlap detection would require converting HH:MM strings into integer minutes, then checking whether the intervals [start, start+duration] of any two tasks intersect. That logic is more complex and harder to debug, and for a basic pet care planner it would be overkill. A pet owner scheduling a morning walk and a feeding 20 minutes apart is a normal, healthy schedule — not a conflict.

    If I were to extend this system in the future, I would upgrade detect_conflicts() to compare time ranges using integer arithmetic so that genuinely overlapping tasks are caught even when their start times differ.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI tools at every stage of this project. During Phase 1, I used AI to brainstorm the four classes (Task, Pet, Owner, Scheduler) and generate the initial Mermaid UML diagram. During Phase 2, I asked AI to flesh out the full implementation of pawpal_system.py including the recurring task logic using timedelta. During Phase 3, I used AI to write the Streamlit UI code in app.py and connect it to my backend using st.session_state. During Phase 5, I asked AI to generate additional pytest cases for conflict detection, recurring tasks, and filter_by_status.

- What kinds of prompts or questions were most helpful?
    - The most helpful prompts were specific and multi-part. For example, asking "give me a complete working Scheduler class with sort_by_time using a lambda key, filter_by_status, filter_by_pet, and detect_conflicts that returns warning strings" gave much better results than a vague request like "write a scheduler." Attaching the existing file as context also helped the AI stay consistent with my existing code style.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
    - One moment where I did not accept the AI suggestion as-is was when it first generated the Task dataclass without a pet_ref field. The AI's initial design had no back-link from a Task to the Pet that owned it. This meant that when mark_complete() tried to auto-schedule the next recurring task, it had no way to know which pet's task list to add it to. I identified this gap by mentally tracing through the logic: if a Task fires mark_complete() and creates a new Task, where does that new Task go? The AI's version just returned the new Task object without adding it anywhere. I modified the design to add a pet_ref field to Task and updated add_task() in Pet to automatically set task.pet_ref = self whenever a task is added. I verified this fix by running test_recurring_daily_task() and confirming the new task appeared in pet.get_tasks() after mark_complete().

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested six core behaviors: task completion status changing to True after mark_complete(), task count increasing when a task is added to a Pet, sort_by_time() returning tasks in chronological order, detect_conflicts() flagging two tasks at the same time, recurring daily tasks auto-creating a new incomplete task after completion, and filter_by_status() returning only incomplete tasks when called with False.

- Why were these tests important?
    These tests were important because they cover the four most critical parts of the system: data integrity (tasks are stored correctly), algorithmic correctness (sorting works), smart logic (recurring tasks and conflict detection), and filtering (the UI depends on filter_by_status to show the right tasks to the user). If any of these broke silently, the app would show wrong information to the pet owner without crashing.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am confident the core scheduling behaviors work correctly based on all 6 tests passing. My confidence level is 4 out of 5 stars.

- What edge cases would you test next if you had more time?
    Edge cases I would test next if I had more time: a pet with zero tasks (does the scheduler crash or return an empty list cleanly?), two pets with tasks at the same time (does detect_conflicts() catch cross-pet conflicts?), a weekly task completing on the last day of the month (does timedelta handle month boundaries correctly?), and a task with an invalid time string like "25:99" entered through the UI.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am most satisfied with how the recurring task logic turned out. The idea that marking a daily feeding as complete automatically schedules tomorrow's feeding — without the owner having to do anything — feels like a genuinely useful feature. Getting that to work cleanly through the pet_ref back-link design was the most satisfying technical moment of the project.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    If I had another iteration, I would redesign conflict detection to use integer minute arithmetic instead of string matching, so that overlapping tasks are caught even when their start times differ. I would also add a persistent data layer using JSON so that pets and tasks are not lost when the Streamlit app restarts. Right now all data lives in st.session_state and disappears on page refresh, which is a significant limitation for a real pet care tool.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    The most important thing I learned is that AI is a powerful first-draft generator but a poor system architect. When I gave AI a vague prompt it produced code that ran but had hidden design gaps, like the missing pet_ref field. When I gave it a precise, structured prompt that described exactly what each method needed to do, it produced code that was much closer to correct. The real engineering work was not writing code — it was knowing what questions to ask, spotting what the AI missed, and making deliberate design decisions like adding due_date and pet_ref that the AI did not think of on its own. Being the lead architect meant staying in charge of the big picture while letting AI handle the repetitive parts.