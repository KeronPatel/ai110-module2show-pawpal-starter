import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Your smart pet care planner.")

# FIX: Use session_state to store owner so data persists between button clicks
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Owner Setup ────────────────────────────────────────────────────────────────
st.subheader("👤 Owner Info")

if st.session_state.owner is None:
    with st.form("owner_form"):
        owner_name = st.text_input("Your name", value="Jordan")
        submitted = st.form_submit_button("Start")
        if submitted and owner_name.strip():
            st.session_state.owner = Owner(owner_name.strip())
            st.success(f"Welcome, {owner_name}!")
            st.rerun()
else:
    st.success(f"Owner: {st.session_state.owner.name}")
    if st.button("Reset everything"):
        st.session_state.owner = None
        st.rerun()

if st.session_state.owner is None:
    st.info("Enter your name above to get started.")
    st.stop()

owner = st.session_state.owner

st.divider()

# ── Add a Pet ──────────────────────────────────────────────────────────────────
st.subheader("🐶 Add a Pet")

with st.form("pet_form"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Biscuit")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
    add_pet = st.form_submit_button("Add Pet")
    if add_pet and pet_name.strip():
        existing = [p.name.lower() for p in owner.pets]
        if pet_name.strip().lower() in existing:
            st.warning(f"{pet_name} is already added.")
        else:
            owner.add_pet(Pet(pet_name.strip(), species))
            st.success(f"Added {pet_name} the {species}!")
            st.rerun()

if owner.pets:
    st.write("**Your pets:**", ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Add a Task ─────────────────────────────────────────────────────────────────
st.subheader("📋 Add a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    with st.form("task_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_pet = st.selectbox(
                "For which pet?",
                [p.name for p in owner.pets]
            )
            description = st.text_input("Task description", value="Morning walk")
            task_time = st.text_input("Time (HH:MM)", value="08:00")
        with col2:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=30
            )
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
            frequency = st.selectbox(
                "Frequency", ["once", "daily", "weekly"], index=1
            )

        add_task = st.form_submit_button("Add Task")

        if add_task:
            # Validate time format
            parts = task_time.strip().split(":")
            valid_time = (
                len(parts) == 2
                and parts[0].isdigit()
                and parts[1].isdigit()
                and 0 <= int(parts[0]) <= 23
                and 0 <= int(parts[1]) <= 59
            )
            if not valid_time:
                st.error("Please enter time in HH:MM format, e.g. 08:00")
            elif not description.strip():
                st.error("Please enter a task description.")
            else:
                pet_obj = next(p for p in owner.pets if p.name == selected_pet)
                new_task = Task(
                    description=description.strip(),
                    time=task_time.strip(),
                    duration=int(duration),
                    priority=priority,
                    frequency=frequency,
                )
                pet_obj.add_task(new_task)
                st.success(
                    f"Added '{description}' for {selected_pet} "
                    f"at {task_time} ({priority} priority)."
                )
                st.rerun()

st.divider()

# ── Schedule View ──────────────────────────────────────────────────────────────
st.subheader("📅 Today's Schedule")

all_tasks = owner.get_all_tasks()

if not all_tasks:
    st.info("No tasks yet. Add some above then generate the schedule.")
else:
    scheduler = Scheduler(owner)

    # Conflict warnings
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(f"⚠️ {warning}")

    if st.button("Generate Schedule 🗓️"):
        sorted_tasks = scheduler.sort_by_time()

        # Build display table
        rows = []
        for task in sorted_tasks:
            # Find which pet owns this task
            pet_name_found = "Unknown"
            for pet in owner.pets:
                if task in pet.get_tasks():
                    pet_name_found = pet.name
                    break

            rows.append({
                "Time": task.time,
                "Pet": pet_name_found,
                "Task": task.description,
                "Duration": f"{task.duration} min",
                "Priority": task.priority.upper(),
                "Frequency": task.frequency,
                "Done": "✓" if task.completed else "○",
            })

        st.table(rows)

    st.divider()

    # Mark tasks complete
    st.subheader("✅ Mark Tasks Complete")
    incomplete = scheduler.filter_by_status(completed=False)

    if not incomplete:
        st.success("All tasks are complete for today!")
    else:
        for i, task in enumerate(incomplete):
            pet_label = "Unknown"
            for pet in owner.pets:
                if task in pet.get_tasks():
                    pet_label = pet.name
                    break
            label = f"{task.time} — {task.description} ({pet_label})"
            if st.button(f"Mark done: {label}", key=f"done_{i}"):
                task.mark_complete()
                st.success(
                    f"'{task.description}' marked complete!"
                    + (" Next occurrence scheduled." if task.frequency != "once" else "")
                )
                st.rerun()

st.divider()
st.caption("PawPal+ — built with Python + Streamlit.")