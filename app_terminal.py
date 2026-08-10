from storage import save_tasks, load_tasks
from datetime import datetime, date
from priority import calculate_priority
from study_planner import create_study_plan

#Welcoming the user to the application
print("Welcome to Ultiplan 365!")
print("Let's add your first task.\n")

#Loading previously saved tasks
tasks = load_tasks()

#Only fixed my previous saved tasks
for task in tasks:
    if "estimated_minutes" not in task:
        task["estimated_minutes"] = 30
save_tasks(tasks)

while True:

    #Collecting information from the user for one task
    while True:
        course = input("Enter your course name: ").strip()
        if course:
            break
        print("Course name cannot be blank.")
    
    while True:
        task_name = input("Enter the task name: ").strip()
        if task_name:
            break
        print("Task name cannot be blank.")

    while True:
        deadline = input("Enter the deadline (YYYY-MM-DD): ").strip()

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()

            if deadline_date < date.today():
                print("The deadline cannot be in the past.")
            else:
                break
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")

    #Letting the user choose an importance level
    print("\nChoose the importance level:")
    print("1. High")
    print("2. Medium")
    print("3. Low")

    while True:
        importance_choice = input("Enter 1, 2, or 3: ").strip()

        #Converting the user's number into an importance label
        if importance_choice == "1":
            importance = "High"
            break

        elif importance_choice == "2":
            importance = "Medium"
            break

        elif importance_choice == "3":
            importance = "Low"
            break

        else:
            print("Please choose 1, 2, or 3.")

    #Letting the user choose a difficulty level
    print("\nChoose the difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        difficulty_choice = input("Enter 1, 2, or 3: ").strip()

        #Converting the user's number into a difficulty label
        if difficulty_choice == "1":
            difficulty = "Easy"
            break

        elif difficulty_choice == "2":
            difficulty = "Medium"
            break

        elif difficulty_choice == "3":
            difficulty = "Hard"
            break

        else:
            print("Please choose 1, 2, or 3.")

    #Adding estimated time the student has during task entry because of the study planner
    while True:
        try:
            estimated_minutes = int(input("How many minutes will it take to finish this task? "))
            if estimated_minutes <= 0:
                print("Please enter a number greater than zero.")
            else:
                break
        except ValueError:
            print("Please enter a valid whole number.")


    #Storing one task information in a dictionary
    task = {
        "course": course,
        "task_name": task_name,
        "deadline": deadline,
        "importance": importance,
        "difficulty": difficulty,
        "estimated_minutes": estimated_minutes
    }

    #Adding task dictionary to the main task list
    tasks.append(task)
    save_tasks(tasks)

    print("\nTask added successfully!")

    #Asking whether the user wants to add another task
    while True:
        add_another = input("\nWould you like to add another task? (yes/no): ").strip().lower()

        if add_another in ["yes", "y"]:
            break

        elif add_another in ["no", "n"]:
            add_another = "no"
            break
                
        else:
            print("Please enter either 'yes' or 'no'.")

    if add_another == "no":
        break

#calculating and saving the priority score for every task
for task in tasks:
    task["priority_score"] = calculate_priority(task)

#Sorting tasks & tie-breaker logic
#1. Highest priority score
#2. Highest deadline
#3. Highest importance
#4. Highest difficulty
# If all values are identical, Python keeps the original entry order.
importance_rank = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

difficulty_rank = {
    "Hard": 3,
    "Medium": 2,
    "Easy": 1
}
tasks.sort(
    key=lambda task: (
        -task["priority_score"],
        task["deadline"],
        -importance_rank[task["importance"]],
        -difficulty_rank[task["difficulty"]]
    )
)

#saving the updated tasks, including the priority scores
save_tasks(tasks)

#Displaying the information back after the user finishes entering them
print("\nYour Tasks:")

for number, task in enumerate(tasks, start=1):
    priority_score = calculate_priority(task)

    print(f"\nTask {number}")
    print(f"course: {task['course']}")
    print(f"Task: {task['task_name']}")
    print(f"Deadline: {task['deadline']}")
    print(f"Importance: {task['importance']}")
    print(f"Difficulty: {task['difficulty']}")
    print(f"Estimated Time: {task['estimated_minutes']} minutes")
    print(f"Priority Score: {task['priority_score']}")

#Displaying the highest-priority task
if tasks:
    focus_task = tasks[0]

    print("\n--- Focus First Recommendation ---")
    print(f"You should work on: {focus_task['task_name']}")
    print(f"Course: {focus_task['course']}")
    print(f"Deadline: {focus_task['deadline']}")
    print(f"Importance: {focus_task['importance']}")
    print(f"Difficulty: {focus_task['difficulty']}")
    print(f"Priority Score: {calculate_priority(focus_task)}")

    print("\nWhy this task?")
    print(
        f"This task has the highest priority because it is due on "
        f"{focus_task['deadline']}, has {focus_task['importance'].lower()} "
        f"importance, and is rated as {focus_task['difficulty'].lower()} difficulty."
    )

#Study plan
#Giving them the plan with the time allocation,
#First step is asking them how much time they'll need
print("\n--- Study Planner ---")

if not tasks:
    print("You need to add at least one task before creating a study plan.")

else:
    while True:
        try:
            available_minutes = int(input("How many total minutes do you have available to study today? "))

            if available_minutes <= 0:
                print("Please enter a number greater than zero.")
            elif available_minutes > 1440:
                print("Please enter 1440 minutes or less.")
            else:
                break
        except ValueError:
            print("Please enter a valid whole number, such as 10, 20, 30 etc.")

    study_plan = create_study_plan(tasks, available_minutes)

    #Displaying today's plan
    print("\nToday's Study Plan")
    
    for i, session in enumerate(study_plan, start=1):

        print(f"\n{i}. {session['task_name']}")
        print(f"Course: {session['course']}")
        print(f"Estimated Time: {session['estimated_minutes']} minutes")
        print(f"Today's Study Time: {session['allocated_minutes']} minutes")
        print(f"Status: {session['status']}")

        if session["status"] == "Continue Tomorrow":
            print(f"Remaining Time: {session['remaining_minutes']} minutes")
    
    #show any unused study time
    used_minutes = sum(session["allocated_minutes"] for session in study_plan)

    leftover_minutes = available_minutes - used_minutes

    if leftover_minutes > 0:
        print(f"\nYou still have {leftover_minutes} minutes available today")


#Task Manager: Completion, Deletion of a tasks.
print("\n--- Task Manager ---")

while True:

    #Checking whether there are any tasks left
    if not tasks:
        print("You currently have no tasks to manage.")
        break
    
    #Displaying every current task
    for number, task in enumerate(tasks, start=1):
        print(f"\n{number}. {task['task_name']}")
        print(f"Course: {task['course']}")
        print(f"Deadline: {task['deadline']}")
    
    print("\nEnter the number of the task you want to manage.")
    print("Enter 0 when you are finished.")

    task_choice = input("Task number: ").strip()

    #Making sure the user enters a whole number
    try:
        task_choice = int(task_choice)
    except ValueError:
        print("Please enter a valid whole number.")
        Continue
    
    #Leaving the Task Manager
    if task_choice == 0:
        break
    
    #Making sure the selected task exists
    if task_choice < 1 or task_choice > len(tasks):
        print("Please choose a task number from the list.")
        continue
    
    #Getting the selected task
    selected_task = tasks[task_choice - 1]

    print(f"\nSelected Task: {selected_task['task_name']}")
    print("\nWhat would you like to do?")
    print("1. Mark as Completed")
    print("2. Delete Task")
    print("3. Cancel")

    action = input("Enter 1, 2, or 3: ").strip()

    #Marking the task as completed
    if action == "1":

        while True:
            confirmation = input(f"Did you complete '{selected_task['task_name']}'? " "(yes/no): ").strip().lower()
            
            if confirmation in ["yes", "y"]:
                tasks.pop(task_choice - 1)
                save_tasks(tasks)

                print(f"\n '{selected_task['task_name']}' " "has been marked as completed!")
                break
            
            elif confirmation in ["no", "n"]:
                print("\nThe task was not marked as completed.")
                break
            
            else:
                print("Please enter either 'yes' or 'no'.")
    
    #Deleting the task
    elif action == "2":

        while True:
            confirmation = input(
                f"Are you sure you want to permanently delete "
                f"'{selected_task['task_name']}'? (yes/no): "
            ).strip().lower()

            if confirmation in ["yes", "y"]:
                tasks.pop(task_choice - 1)
                save_tasks(tasks)

                print(f"\n'{selected_task['task_name']}'" "has been deleted successfully")
                break
            
            elif confirmation in ["no", "n"]:
                print("\nThe task was not deleted.")
                break
            
            else:
                print("Please enter either 'yes' or 'no'.")

    #Canceling the action
    elif action == "3":
        print("\nNo changes were made.")
    
    else:
        print("\nPlease choose 1, 2, or 3.")


#Ending the application
print("=" * 35)
print("Thank you for using Ultiplan 365!")
print("Good luck with your studies today.")
print("=" * 35)

    