# UltiPlan 365

UltiPlan 365 is a student task-prioritization and study-planning web application built with Python and Flask.

The application helps students organize assignments, calculate task priorities, create study plans based on available time, focus on important work, and manage both active and completed tasks.

---

## Project Purpose

Students often have several assignments, exams, and study responsibilities at the same time. It can be difficult to decide what to work on first, especially when each task has a different deadline, importance level, difficulty, and estimated completion time.

UltiPlan 365 was created to make that process easier by giving students one place to:

- Add and organize tasks
- Calculate task priority
- Review current work
- Create a study plan
- Focus on the most important task
- Track completed tasks
- Manage their app preferences

---

## Main Features

### Dashboard

The Dashboard gives the user a clear overview of their current workload.

It displays:

- Total number of tasks
- Number of active tasks
- Number of completed tasks
- Number of high-priority tasks
- Current tasks in priority order
- The highest-priority task
- Total estimated study time
- Average priority score
- Nearest task deadline
- Quick links to the main planning tools

---

### Add Task

The Add Task page allows the user to enter:

- Task name
- Course or subject
- Deadline
- Estimated completion time
- Importance
- Difficulty

The page also includes:

- A working Save Task button
- A working Save and Add Another button
- A live task-name character counter
- A live priority-score preview
- A real daily progress circle
- Planning tips
- Input validation for dates and estimated time

The priority preview updates as the user selects a deadline, importance level, and difficulty level.

---

### View Tasks

The View Tasks page displays all active tasks in priority order.

It includes:

- Task name
- Course
- Deadline
- Estimated time
- Difficulty
- Importance
- Priority score
- Search by task name or course
- Task importance summary
- A direct link to the Study Planner

---

### Study Planner

The Study Planner creates a focused plan based on the amount of time the user has available.

The user enters the number of minutes they can study, and the application assigns that time to tasks using their current priority order.

The study plan shows:

- Task order
- Time assigned to each task
- Whether the task can be completed today
- Whether part of the task should continue later
- Remaining task time
- Total planned study time
- Any unused time

---

### Focus First

Focus First helps the user begin with the highest-priority active task.

The page displays:

- Task name
- Course
- Deadline
- Estimated time
- Importance
- Difficulty
- Priority score
- The reason the task was selected first

The focus timer includes three methods:

- Pomodoro: 25-minute focus session and 5-minute break
- Deep Focus: 45-minute focus session and 10-minute break
- Long Session: 60-minute focus session and 15-minute break

Focus First also includes:

- Start and pause controls
- Reset button
- Optional suggested breaks
- A moving circular timer
- Task-time progress tracking
- Skip Task button
- Move to the next priority task
- A completion message when the estimated task time is reached
- Continue Working option
- Move to Next Task option

Break time is tracked separately and does not count as work completed on the task.

---

### Task Manager

The Task Manager allows the user to manage both active and completed tasks.

Users can:

- Mark an active task as completed
- Move completed tasks back to active tasks
- Delete an active task
- Remove a completed task from history
- Review active, completed, and total task counts
- Review task-completion progress
- See a progress percentage and progress bar

Active tasks are stored separately from completed tasks.

---

### Settings

The Settings page allows the user to customize the application.

Available settings include:

- Light theme
- Dark theme
- Normal text size
- Large text size
- Default Focus First method
- Suggested breaks on or off
- Reduce Motion
- Reset Preferences

Settings are saved in the browser using `localStorage`, so they remain active when the user changes pages or refreshes the application.

---

## Priority Score System

Each task receives a priority score based on three factors:

1. Deadline
2. Importance
3. Difficulty

The deadline, importance, and difficulty points are added together to create the final priority score. Tasks with higher scores appear first.

---

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Jinja templates
- JSON
- Browser localStorage
- GitHub Codespaces

---

## Project Structure

UltiPlan-365/
│
├── app.py
├── app_terminal.py
├── priority.py
├── storage.py
├── study_planner.py
├── task_logic.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── tasks.json
│   └── completed_tasks.json
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── script.js
│       └── settings.js
│
└── templates/
    ├── index.html
    ├── add_task.html
    ├── view_tasks.html
    ├── study_planner.html
    ├── focus_first.html
    ├── task_manager.html
    └── settings.html


---

## How Task Data Is Stored

UltiPlan 365 uses JSON files to store task information locally.

### Active Tasks

Active tasks are stored in:

data/tasks.json

### Completed Tasks

Completed tasks are stored in:

data/completed_tasks.json

When a task is marked as completed, it is removed from the active-task file and added to the completed-task file.

When a completed task is moved back to active, it is returned to `tasks.json` and sorted again by priority.

---

## How to Run the Application

### 1. Open the project folder

```bash
cd /workspaces/UltiPlan-365
```

### 2. Install the required packages

```bash
pip install -r requirements.txt
```

### 3. Start the Flask application

```bash
python app.py
```

### 4. Open the application

Open the local address shown in the terminal.

When using GitHub Codespaces, open the forwarded Flask port from the Ports section.

---

## How to Use UltiPlan 365

1. Open the Add Task page.
2. Enter the task name, course, deadline, estimated time, importance, and difficulty.
3. Save the task.
4. Review the saved task on the Dashboard or View Tasks page.
5. Use the Study Planner to organize your available study time.
6. Use Focus First to begin with the highest-priority task.
7. Use Task Manager to complete, restore, or delete tasks.
8. Use Settings to change the theme, text size, default focus method, and break preference.

---

## Input Validation

UltiPlan 365 checks for common input errors before saving a task.

The application checks for:

- Blank task names
- Blank course names
- Invalid deadlines
- Deadlines in the past
- Invalid estimated time
- Estimated time that is less than or equal to zero

When an input is invalid, the user receives a message explaining what needs to be corrected.

---

## Current MVP Status

The current minimum viable product includes:
- Adding a task with a course, task name, deadline, importance, difficulty, and estimated time
- Checking user input before saving a task
- Saving active tasks in a JSON file
- Calculating a priority score based on deadline, importance, and difficulty
- Sorting tasks from highest to lowest priority
- Displaying all saved tasks
- Recommending the highest-priority task through Focus First
- Creating a study plan based on the user’s available study time
- Using a focus timer while working on a task
- Marking tasks as completed
- Moving completed tasks back to the active-task list
- Deleting active and completed tasks
- Saving completed tasks separately from active tasks

These features complete the main purpose of UltiPlan 365: helping students organize their work, prioritize tasks, plan their study time, and stay focused.

---

## Additional Features

After completing the main MVP, I added several improvements to make the application easier and more enjoyable to use.

These additions include:

- Task search
- Save and Add Another
- Live priority-score preview
- Daily progress display
- Multiple focus methods
- Optional breaks
- Light and dark themes
- Text-size preferences
- Reduce Motion
- Saved settings using browser localStorage
- Responsive and consistent page designs

---

## Future Improvements

Possible future additions include:

- User accounts and login
- Importing tasks
- Task categories
- Task notes
- Deadline reminders
- Calendar integration
- Editing existing tasks
- Saving Focus First progress after refreshing
- More detailed task analytics
- Mobile notifications
- Cloud database storage
- Multiple student profiles

These features are not required for the current MVP, but they could be added in future versions of UltiPlan 365.

---

## Challenges and Learning

Some of the most challenging parts of the project included:

- Connecting Flask routes to HTML forms
- Keeping active and completed tasks in separate JSON files
- Matching Flask route names with 'url_for()'
- Debugging variable-name errors
- Building a JavaScript countdown timer
- Connecting focus sessions to a task’s estimated time
- Adding optional breaks
- Making the circular timer progress move correctly
- Passing Python task data into JavaScript
- Saving settings with 'localStorage'
- Applying light and dark themes across every page
- Keeping the page layouts consistent
- Making features work without making the code too complicated

Working through these challenges helped me improve my understanding of Python, Flask, JSON storage, HTML, CSS, JavaScript, debugging, and web-application structure.

---

## Author

**Moyinoluwa Ajibade**

Student developer and creator of UltiPlan 365.

---

## Version

**UltiPlan 365 MVP**  
Version 1.0  
2026