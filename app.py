from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash

from storage import (load_tasks, save_tasks, load_completed_tasks, save_completed_tasks) 
from task_logic import create_task, sort_tasks
from study_planner import create_study_plan

app = Flask(__name__)

#Flask needs a secret key to display temporary messages
app.secret_key = "ultiplan365-secret-key"

#Calculate the percentage of completed tasks
def calculate_daily_progress():
    active_tasks = load_tasks()
    completed_tasks = load_completed_tasks()

    total_tasks = len(active_tasks) + len(completed_tasks)

    if total_tasks == 0:
        return 0
    
    return round(
        len(completed_tasks) / total_tasks * 100
    )

@app.route("/")
def home():
    #Loading active and completed tasks
    tasks = load_tasks()
    completed_task_list = load_completed_tasks()

    #Keep active tasks in priority order
    sort_tasks(tasks)
    active_count = len(tasks)
    completed_count = len(completed_task_list)
    total_count = active_count + completed_count

    #Counting active tasks marked as high priority
    high_priority_count = 0

    for task in tasks:
        if task["importance"] == "High":
            high_priority_count += 1
    
    #The first task is the Focus First recommendation
    focus_task = tasks[0] if tasks else None
    
    #Showing only the first four tasks on the dashboard
    dashboard_tasks = tasks[:4]

    #Calculating the total estimated time for active tasks
    total_estimated_minutes = 0

    for task in tasks:
        total_estimated_minutes += task["estimated_minutes"]
    
    #Calculating the average priority score
    if tasks:
        total_priority_score = 0

        for task in tasks:
            total_priority_score += task["priority_score"]
        
        average_priority_score = round(
            total_priority_score / len(tasks)
        )
    else:
        average_priority_score = 0
    
    #Finding task with the nearest deadline
    if tasks:
        next_deadline_task = min(
            tasks,
            key=lambda task: task["deadline"]
        )
    else:
        next_deadline_task = None

    #Sending the tasks and dashboard info to index.html
    return render_template(
        "index.html",
        tasks=dashboard_tasks,
        active_count=active_count,
        completed_count=completed_count,
        total_count=total_count,
        high_priority_count=high_priority_count,
        focus_task=focus_task,
        total_estimated_minutes=total_estimated_minutes,
        average_priority_score=average_priority_score,
        next_deadline_task=next_deadline_task
    )

@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    #showing the user's real completed-task progress
    daily_progress = calculate_daily_progress()

    if request.method == "POST":
        course = request.form["course"].strip()
        task_name = request.form["task_name"].strip()
        deadline = request.form["deadline"]
        importance = request.form["importance"]
        difficulty = request.form["difficulty"]

        #Telling Flask which save button was selected
        save_action = request.form.get(
            "save_action",
            "save"
        )

        try:
            estimated_minutes = int(
                request.form["estimated_minutes"]
            )
        except ValueError:
            return render_template(
                "add_task.html",
                error="Please enter a valid whole number",
                daily_progress=daily_progress
            )
        
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            return render_template(
                "add_task.html",
                error="Please enter a valid deadline.",
                daily_progress=daily_progress
            )

        if deadline_date < date.today():
            return render_template(
                "add_task.html",
                error="The deadline cannot be in the past.",
                daily_progress=daily_progress
            ) 
        
        if not course or not task_name:
            return render_template(
                "add_task.html",
                error="Course and task name cannot be blank.",
                daily_progress=daily_progress
            )
        
        if estimated_minutes <= 0:
            return render_template(
                "add_task.html",
                error="Estimated time must be greater than zero.",
                daily_progress=daily_progress
            )
        
        task = create_task(
            course,
            task_name,
            deadline,
            importance,
            difficulty,
            estimated_minutes

        )

        tasks = load_tasks()
        tasks.append(task)

        sort_tasks(tasks)
        save_tasks(tasks)

        flash("Task added successfully!")

        #Saving the task and returning to a clean Add Task form
        if save_action == "save_another":
            return redirect(url_for("add_task"))

        #Normal save Task button returns to the dashboard
        return redirect(url_for("home"))

    return render_template(
        "add_task.html",
        daily_progress=daily_progress
    )

#Open the page that displays all saved tasks
@app.route("/view-tasks")

def view_tasks():
    #Loading the tasks saved inside tasks.json
    tasks = load_tasks()

    #Sending the task list to the View Tasks page
    return render_template("view_tasks.html", tasks=tasks)
#Opening the Study Planner Page and processing available study time
@app.route("/study-planner", methods=["GET", "POST"])

def study_planner():
    # Loading the saved tasks from tasks.json
    tasks = load_tasks()

    #These values are empty when the page first opens
    study_plan = None
    available_minutes = None
    used_minutes = 0
    leftover_minutes = 0
    error = None

    #Running this section after the user submits the form
    if request.method == "POST":
        try:
            # Converting the form entry into a whole number
            available_minutes = int(request.form["available_minutes"])
            #Making sure the entered time is within the allowed range
            if available_minutes <= 0:
                error = "Please enter a number grater than zero."
            elif available_minutes > 1440:
                error = "Please enter 1440 minutes or less."

            #A study plan cannot be created without saved tasks
            elif not tasks:
                error = "Please add at least one task before creating a study plan."
            else:
                #Using the original Study Planner Logic from my terminal MVP
                study_plan = create_study_plan(tasks, available_minutes)
                #Adding together the time assigned to each study session
                used_minutes = sum(session["allocated_minutes"] for session in study_plan)
                #Calculating any time that was not assigned
                leftover_minutes = (available_minutes - used_minutes)
        except ValueError:
            error = "Please enter a valid whole number"

    #Displaying the page and sending planner results to the HTML
    return render_template(
        "study_planner.html",
        study_plan=study_plan,
        available_minutes=available_minutes,
        used_minutes=used_minutes,
        leftover_minutes=leftover_minutes,
        error=error
    )

#Opening the Focus First Page
@app.route("/focus-first")
def focus_first():
    # Load and sort every task so the user can move to the next task
    tasks = load_tasks()
    sort_tasks(tasks)

    # The first task is the highest-priority task
    focus_task = tasks[0] if tasks else None

    return render_template(
        "focus_first.html",
        focus_task=focus_task,
        tasks=tasks
    )

#Opening the page used to complete or delete tasks
@app.route("/task-manager")
def task_manager():
    #Loading active and completed tasks
    tasks = load_tasks()
    completed_tasks = load_completed_tasks()

    return render_template(
        "task_manager.html", 
        tasks=tasks,
        completed_tasks=completed_tasks,
        active_count=len(tasks),
        completed_count=len(completed_tasks),
        total_count=len(tasks) + len(completed_tasks)
    )

@app.route("/complete-tasks/<int:task_index>", methods=["POST"])
def complete_task(task_index):
    #Loading the current active tasks
    tasks = load_tasks()

    #Making sure the selected task exists
    if 0 <= task_index < len(tasks):
        completed_task = tasks.pop(task_index)

        #Adding a completed status to the task
        completed_task["status"] = "Completed"

        completed_tasks = load_completed_tasks()
        completed_tasks.append(completed_task)

        #save both lists
        save_tasks(tasks)
        save_completed_tasks(completed_tasks)

        flash("Task marked as completed!")
    return redirect(url_for("task_manager"))

@app.route("/delete-task/<int:task_index>", methods=["POST"])
def delete_tasks(task_index):
    #Loading the active tasks
    tasks = load_tasks()
    #Deleting the selected task
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        save_tasks(tasks)

        flash("Task deleted successfully.")
    return redirect(url_for("task_manager"))

@app.route("/delete-completed-task/<int:task_index>", methods=["POST"])
def delete_completed_task(task_index):
    #Loading completed tasks
    completed_tasks = load_completed_tasks()

    #Deleting the selected completed task
    if 0 <= task_index < len(completed_tasks):
        completed_tasks.pop(task_index)
        save_completed_tasks(completed_tasks)

        flash("Completed task removed.")
    return redirect(url_for("task_manager"))

@app.route("/restore-completed-task/<int:task_index>", methods=["POST"])
def restore_completed_task(task_index):
    #Loading both active and completed tasks
    tasks = load_tasks ()
    completed_tasks = load_completed_tasks()

    #Making sure the selected completed task exists
    if 0 <= task_index < len(completed_tasks):
        restored_task = completed_tasks.pop(task_index)

        #Removing the completed status before returning it to active tasks
        restored_task.pop("status", None)

        #Add it back to the active task list
        tasks.append(restored_task)

        #Sort the active tasks again by priority
        sort_tasks(tasks)

        #Saving both updated lists
        save_tasks(tasks)
        save_completed_tasks(completed_tasks)

        flash("Task moved back to active tasks.")
    return redirect(url_for("task_manager"))

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)