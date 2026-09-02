import json
import os

TASK_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with open(TASK_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def view_tasks(tasks):
    print("\n========== YOUR TASKS ==========")

    if not tasks:
        print("📭 No tasks found.")
        return

    for index, task in enumerate(tasks, start=1):
        status = "✅" if task["completed"] else "⬜"
        print(f"{index}. {status} {task['title']}")


def add_task(tasks):
    title = input("\nEnter task: ").strip()

    if not title:
        print("❌ Task cannot be empty.")
        return

    tasks.append({
        "title": title,
        "completed": False
    })

    save_tasks(tasks)
    print("✅ Task added successfully!")


def delete_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        task_number = int(input("\nEnter task number to delete: "))

        if 1 <= task_number <= len(tasks):
            deleted_task = tasks.pop(task_number - 1)
            save_tasks(tasks)
            print(f"🗑️ Deleted: {deleted_task['title']}")
        else:
            print("❌ Invalid task number.")

    except ValueError:
        print("❌ Please enter a valid number.")


def complete_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        task_number = int(input("\nEnter task number to mark complete: "))

        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1]["completed"] = True
            save_tasks(tasks)
            print("✅ Task marked as completed!")
        else:
            print("❌ Invalid task number.")

    except ValueError:
        print("❌ Please enter a valid number.")


def todo_app():
    tasks = load_tasks()

    while True:
        print("\n================================")
        print("          TO-DO LIST")
        print("================================")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Delete Task")
        print("5. Exit")
        print("================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            complete_task(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            print("\n👋 To-Do List closed. Thank you!")
            break

        else:
            print("❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    todo_app()