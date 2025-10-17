#! /usr/bin/env python3

import json
from pathlib import Path
import sys

# ==============================
# Constants
# ==============================

PATH = Path.cwd()
FILE = PATH / "todos.json"

# ==============================
# Functions
# ==============================

def check_todos_exist(create_if_missing=True):
    """Check if todos.json exists, and create if not."""
    if not FILE.is_file() and create_if_missing:
        create_todos()

def create_todos():
    """Create an empty todos.json."""
    Path("todos.json").touch()

def process(*args):
    """Base program process on first arg."""
    if not args:
        print_help()
        sys.exit(1)
    elif args[0] == "list" and len(args) == 1:
        check_todos_exist(create_if_missing=False)
        list_tasks()
    elif args[0] == "add" and len(args) == 2:
        check_todos_exist()
        add_task(args[1])
    elif args[0] == "update" and len(args) == 3:
        check_todos_exist(create_if_missing=False)
        update_task(args[1], args[2])
    elif args[0] == "delete" and len(args) == 2:
        check_todos_exist(create_if_missing=False)
        delete_task(args[1])
    elif args[0] == "mark-in-progress" and len(args) == 2:
        check_todos_exist(create_if_missing=False)
        set_status(args[1], "in progress")
    elif args[0] == "mark-done" and len(args) == 2:
        check_todos_exist(create_if_missing=False)
        set_status(args[1], "done")
    else:
        print_help()
        sys.exit(1)

def print_help():
    """Prints a help message."""
    print("Usage: task-cli.py <command>")
    print()
    print("Commands:    list                        - lists existing todos")
    print("             add '[TASK]'                - add a new todo")
    print("             update [TASK-ID] '[TASK]'   - update an existing todo")
    print("             delete [TASK-ID]            - delete an existing todo")
    print("             mark-in-progress [TASK-ID]  - mark an existing todo 'in progress'")
    print("             mark-done [TASK-ID]         - mark an existing todo 'done'")
    print()

def if_no_tasks(tasks):
    if not tasks:
        print("No existing task(s).")
        sys.exit(1)

def load_tasks():
    """Load tasks from todos.json, return a list of dicts"""#
    if not FILE.is_file():
        return []
    with FILE.open("r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Save list of task dicts to todos.json."""
    with FILE.open("w") as f:
        json.dump(tasks, f, indent=4)

def renumber_tasks(tasks):
    for idx, task in enumerate(tasks, start=1):
        task['id'] = idx
    save_tasks(tasks)
    return tasks

def list_tasks():
    """Lists all existing tasks."""
    if not FILE.is_file():
        print("No existing task(s).")
        sys.exit(1)
    tasks = load_tasks()
    if_no_tasks(tasks)
    for t in tasks:
        print(f"{t['id']}: {t['task']} [{t['status']}]")

def add_task(task: str):
    """Add a new task, respecting existing JSON and auto-increment ID."""
    tasks = load_tasks()

    if tasks:
        next_id = max(task["id"] for task in tasks) + 1
    else:
        next_id = 1

    new_task = {
        "id": next_id,
        "task": task,
        "status": "pending"
    }

    tasks.append(new_task)
    save_tasks(tasks)

def update_task(id: str, task: str):
    """Update the content of an existing task."""
    try:
        task_id = int(id)
    except ValueError:
        print("Task-ID has to be a number.")
        sys.exit(1)
    tasks = load_tasks()

    if_no_tasks(tasks)
    
    for t in tasks:
        if t['id'] == task_id:
            t['task'] = task
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return
    
    print(f"No task found with ID: {task_id}")
    sys.exit(1)

def delete_task(id: str):
    """Delete existing task by ID."""
    try:
        task_id = int(id)
    except ValueError:
        print("Task-ID has to be a number.")
        sys.exit(1)
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task['id'] != task_id]

    if_no_tasks(tasks)

    if len(new_tasks) == len(tasks):
        print(f"No task found with ID: {task_id}")
        sys.exit(1)

    renumber_tasks(new_tasks)
    print(f"Task {task_id} deleted.") 

def set_status(id: str, status: str):
    """Sets status for given task."""
    try:
        task_id = int(id)
    except ValueError:
        print("Task-ID has to be a number.")
        sys.exit(1)
    tasks = load_tasks()
    if_no_tasks(tasks)
    for t in tasks:
        if t['id'] == task_id:
            t['status'] = status
            save_tasks(tasks)
            print(f"Set status to '{status}' for task {task_id}")
            return
    print(f"No task found with ID: {task_id}")
    sys.exit(1)

# ==============================
# Main
# ==============================

if __name__ == '__main__':
    process(*sys.argv[1:])
