import json
import os


#File used for active tasks
TASk_FILE = "data/tasks.json"

#File used for completed tasks
COMPLETED_TASK_FILE = "data/completed_tasks.json"

#Loading active tasks
def load_tasks():
    if not os.path.exists(TASk_FILE):
        return []
    
    try:
        with open(TASk_FILE, "r") as file:
            return json.load(file)
    
    except json.JSONDecodeError:
        return[]

#saving active tasks
def save_tasks(tasks):
    os.makedirs("data", exist_ok=True)
    with open(TASk_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

#Loading completed tasks
def load_completed_tasks():
    if not os.path.exists(COMPLETED_TASK_FILE):
        return []
    try:
        with open(COMPLETED_TASK_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


#Saving completed tasks
def save_completed_tasks(tasks):
    os.makedirs("data", exist_ok=True)

    with open(COMPLETED_TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)