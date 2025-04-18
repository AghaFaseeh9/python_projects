import click  # to create a CLI
import json  # to save and load tasks from a file
import os  # to check if file exists

TODO_FILE = "todos.json"


def load_tasks():
    if not os.path.exists(TODO_FILE):  # Fix: Corrected logic
        return []
    with open(TODO_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


@click.group()
def cli():
    """Simple To-Do List Manager"""
    pass


@click.command()
@click.argument("task")
def add(task):
    """Add a new Task to the List"""
    tasks = load_tasks()
    tasks.append({"Task": task, "done": False})
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")


@click.command()
def list_tasks():
    """List all the Tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found.")
        return
    for index, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "Not Done"
        click.echo(f"{index}. {task['Task']} [{status}]")  # Fix: Corrected key


@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed")
    else:
        click.echo(f"Invalid Task Number: {task_number}")


@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks()  # Fix: Added parentheses to call function properly
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)  # Fix: Corrected pop() method
        save_tasks(tasks)
        click.echo(f"Removed Task: {removed_task['Task']}")  # Fix: Corrected key
    else:
        click.echo(f"Invalid Task Number: {task_number}")

# Register commands
cli.add_command(add)
cli.add_command(list_tasks)
cli.add_command(complete)
cli.add_command(remove)

if __name__ == "__main__":
    cli()
