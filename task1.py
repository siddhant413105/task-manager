
import sys
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

tasks = []

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            global tasks
            tasks = json.load(file)
    except FileNotFoundError:
        pass

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def add_task(task, due_date=None, priority=None, category=None):
    task_details = {"task": task, "completed": False, "due_date": due_date, "priority": priority, "category": category}
    tasks.append(task_details)
    print(f'Added task: {task}')
    view_tasks_ui()

def delete_task(task_index):
    try:
        removed_task = tasks.pop(task_index)
        print(f'Deleted task: {removed_task["task"]}')
        view_tasks_ui()
    except IndexError:
        print("Invalid task number")

def view_tasks():
    if not tasks:
        print("No tasks available")
    else:
        for i, task in enumerate(tasks):
            status = "Completed" if task["completed"] else "Pending"
            due_date = task["due_date"] if task["due_date"] else "No due date"
            priority = task["priority"] if task["priority"] else "No priority"
            category = task["category"] if task["category"] else "No category"
            print(f'{i + 1}. {task["task"]} [{status}] - Due: {due_date} - Priority: {priority} - Category: {category}')

def mark_task_completed(task_index):
    try:
        tasks[task_index]["completed"] = True
        print(f'Marked task as completed: {tasks[task_index]["task"]}')
        view_tasks_ui()
    except IndexError:
        print("Invalid task number")

def search_tasks(keyword):
    results = [task for task in tasks if keyword.lower() in task["task"].lower()]
    if not results:
        print("No matching tasks found")
    else:
        for i, task in enumerate(results):
            status = "Completed" if task["completed"] else "Pending"
            due_date = task["due_date"] if task["due_date"] else "No due date"
            priority = task["priority"] if task["priority"] else "No priority"
            category = task["category"] if task["category"] else "No category"
            print(f'{i + 1}. {task["task"]} [{status}] - Due: {due_date} - Priority: {priority} - Category: {category}')

def show_help():
    help_message = """
    Available commands:
    - add <task> <due_date (YYYY-MM-DD)> <priority> <category>: Add a new task with optional due date, priority, and category
    - delete <task_number>: Delete a task by its number
    - view: View all tasks
    - complete <task_number>: Mark a task as completed
    - search <keyword>: Search for tasks by keyword
    - help: Show this help message
    - exit: Exit the application
    """
    messagebox.showinfo("Help", help_message)

def exit_application():
    save_tasks()
    print("Exiting the application. Goodbye!")
    sys.exit()

def add_task_ui(task, due_date, priority, category):
    add_task(task, due_date, priority, category)
    messagebox.showinfo("Success", f'Added task: {task}')
    view_tasks_ui()

def delete_task_ui(task_index):
    try:
        removed_task = tasks.pop(task_index)
        messagebox.showinfo("Success", f'Deleted task: {removed_task["task"]}')
        view_tasks_ui()
    except IndexError:
        messagebox.showerror("Error", "Invalid task number")

def mark_task_completed_ui(task_index):
    try:
        tasks[task_index]["completed"] = True
        messagebox.showinfo("Success", f'Marked task as completed: {tasks[task_index]["task"]}')
        view_tasks_ui()
    except IndexError:
        messagebox.showerror("Error", "Invalid task number")

def view_tasks_ui():
    for row in task_tree.get_children():
        task_tree.delete(row)
    if not tasks:
        task_tree.insert("", "end", values=("No tasks available", "", "", "", ""))
    else:
        for i, task in enumerate(tasks):
            status = "Completed" if task["completed"] else "Pending"
            due_date = task["due_date"] if task["due_date"] else "No due date"
            priority = task["priority"] if task["priority"] else "No priority"
            category = task["category"] if task["category"] else "No category"
            task_tree.insert("", "end", values=(i + 1, task["task"], status, due_date, priority, category))

def main_ui():
    global task_tree

    root = tk.Tk()
    root.title("Advanced Task Manager")

    tk.Label(root, text="Advanced Task Manager Application", font=("Helvetica", 16)).pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Task:").grid(row=0, column=0)
    task_entry = tk.Entry(input_frame, width=50)
    task_entry.grid(row=0, column=1, padx=10)

    tk.Label(input_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0)
    due_date_entry = tk.Entry(input_frame, width=20)
    due_date_entry.grid(row=1, column=1, padx=10)

    tk.Label(input_frame, text="Priority:").grid(row=2, column=0)
    priority_entry = tk.Entry(input_frame, width=20)
    priority_entry.grid(row=2, column=1, padx=10)

    tk.Label(input_frame, text="Category:").grid(row=3, column=0)
    category_entry = tk.Entry(input_frame, width=20)
    category_entry.grid(row=3, column=1, padx=10)

    tk.Button(input_frame, text="Add Task", command=lambda: add_task_ui(task_entry.get(), due_date_entry.get(), priority_entry.get(), category_entry.get())).grid(row=4, column=0, columnspan=2, pady=10)

    task_tree = ttk.Treeview(root, columns=("Number", "Task", "Status", "Due Date", "Priority", "Category"), show="headings")
    task_tree.heading("Number", text="Number")
    task_tree.heading("Task", text="Task")
    task_tree.heading("Status", text="Status")
    task_tree.heading("Due Date", text="Due Date")
    task_tree.heading("Priority", text="Priority")
    task_tree.heading("Category", text="Category")
    task_tree.pack(pady=10)

    view_tasks_ui()

    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    tk.Label(control_frame, text="Task Number:").grid(row=0, column=0)
    task_number_entry = tk.Entry(control_frame, width=5)
    task_number_entry.grid(row=0, column=1, padx=10)

    tk.Button(control_frame, text="Delete Task", command=lambda: delete_task_ui(int(task_number_entry.get()) - 1)).grid(row=0, column=2)
    tk.Button(control_frame, text="Complete Task", command=lambda: mark_task_completed_ui(int(task_number_entry.get()) - 1)).grid(row=0, column=3)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="View Tasks", command=view_tasks_ui).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Help", command=show_help).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Exit", command=exit_application).pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    load_tasks()
    main_ui()
