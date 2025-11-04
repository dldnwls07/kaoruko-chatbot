import sys
import os

def update_todo_list(task_description):
    """
    Marks a task in the TODO.md file on the Desktop as completed.
    """
    try:
        # Construct the full path to the TODO.md file on the user's Desktop
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        todo_file_path = os.path.join(desktop_path, "TODO.md")

        if not os.path.exists(todo_file_path):
            print(f"Error: TODO.md not found at {todo_file_path}")
            return

        with open(todo_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        updated = False
        new_lines = []
        # Find the specific task line to update
        task_line_to_find = f"- [ ] {task_description}"

        for i, line in enumerate(lines):
            # Strip whitespace to ensure accurate comparison
            if line.strip() == task_line_to_find.strip():
                lines[i] = line.replace('- [ ]', '- [x]', 1)
                updated = True
                break # Stop after finding and updating the first match

        if updated:
            with open(todo_file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Successfully updated task: '{task_description}'")
        else:
            print(f"Warning: Task not found or already completed: '{task_description}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_todo.py \"<task description to complete>\"")
    else:
        # Join all arguments after the script name to form the task description
        task_to_complete = " ".join(sys.argv[1:])
        update_todo_list(task_to_complete)
