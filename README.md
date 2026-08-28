# UltiPlan 365

UltiPlan 365 is a multi-user student productivity, task-prioritization, and study-planning web application built with Python and Flask.

The application helps students organize assignments, prioritize their workload, create study plans based on available time, focus on important work, and manage their academic tasks from one personalized account.

---

## Project Purpose

Students often have several assignments, exams, projects, and other responsibilities competing for their attention at the same time.

Even when students know what they need to complete, deciding **what to work on first** can be difficult.

UltiPlan 365 was created to make that process easier.

The application gives students one place to:

- Create their own account
- Add and organize academic tasks
- Calculate task priorities
- Review upcoming work
- Create study plans based on available time
- Focus on the most important task
- Use timed focus sessions
- Track completed tasks
- Manage personal study preferences
- Update and manage their account

Each user's tasks are connected to their individual account, allowing multiple students to use the application without sharing task data.

---

# Main Features

## User Accounts and Authentication

UltiPlan 365 includes a complete account system that allows each student to have an individual experience.

Users can:

- Register for an account
- Log in using their email and password
- Log out securely
- Access protected pages only after logging in
- Edit their name and email
- Change their password
- Reset a forgotten password through email
- Permanently delete their account

Passwords are stored as password hashes rather than plain-text passwords.

User authentication and protected routes are managed using Flask-Login.

---

## Password Reset

Users who forget their password can request a password-reset email from the login system.

The password-reset process includes:

1. Entering the account email address
2. Receiving a password-reset link by email
3. Opening a secure reset page
4. Creating and confirming a new password
5. Returning to the login page
6. Logging in with the new password

Password-reset links use time-limited tokens and expire after **30 minutes**.

The application also avoids revealing whether an email address is registered when a password-reset request is submitted.

---

## Dashboard

The Dashboard gives each user an overview of their current workload.

It displays:

- Total number of tasks
- Number of active tasks
- Number of completed tasks
- Number of high-priority tasks
- Current tasks in priority order
- Highest-priority task
- Total estimated study time
- Average priority score
- Nearest task deadline
- Quick links to the main planning tools

Dashboard information is calculated using only the tasks belonging to the currently logged-in user.

---

## Add Task

The Add Task page allows users to enter:

- Task name
- Course or subject
- Deadline
- Estimated completion time
- Importance
- Difficulty

The page also includes:

- Save Task
- Save and Add Another
- Live task-name character counter
- Live priority-score preview
- Daily progress display
- Planning tips
- Input validation

The priority preview changes as the user selects a deadline, importance level, and difficulty level.

Tasks are automatically connected to the account of the user who creates them.

---

## View Tasks

The View Tasks page displays the logged-in user's active tasks in priority order.

Task information includes:

- Task name
- Course
- Deadline
- Estimated time
- Difficulty
- Importance
- Priority score

The page also includes:

- Search by task name or course
- Task importance summary
- Direct access to the Study Planner

Users only see tasks associated with their own account.

---

## Study Planner

The Study Planner creates a focused study plan based on how much time the student currently has available.

The user enters the number of minutes available for studying, and UltiPlan 365 assigns that time to active tasks according to their priority.

The generated study plan shows:

- Task order
- Time assigned to each task
- Whether a task can be completed during the available time
- Whether part of a task should continue later
- Remaining task time
- Total planned study time
- Unused study time

This allows students to turn a limited amount of available time into a structured study session.

---

## Focus First

Focus First helps students answer one important question:

**What should I work on first?**

The application identifies the user's highest-priority active task and places it at the center of the focus experience.

The page displays:

- Task name
- Course
- Deadline
- Estimated time
- Importance
- Difficulty
- Priority score
- Reason the task was selected

### Focus Methods

Users can choose between three focus methods:

- **Pomodoro** — 25-minute focus session with a 5-minute break
- **Deep Focus** — 45-minute focus session with a 10-minute break
- **Long Session** — 60-minute focus session with a 15-minute break

Focus First also includes:

- Start and pause controls
- Reset control
- Optional suggested breaks
- Circular timer progress
- Task-time progress tracking
- Skip Task
- Move to the next priority task
- Completion message when estimated task time is reached
- Continue Working
- Move to Next Task

Break time is tracked separately and does not count toward completed task work time.

---

## Task Manager

The Task Manager allows students to manage both active and completed tasks.

Users can:

- Mark active tasks as completed
- Restore completed tasks
- Delete active tasks
- Remove completed tasks from their history
- Review active-task counts
- Review completed-task counts
- Review total task counts
- View completion progress
- View a progress percentage and progress bar

All task-management actions are restricted to tasks belonging to the currently logged-in user.

---

# Settings

The Settings page gives students control over both their study preferences and their account.

## App Preferences

Users can customize:

- Light theme
- Dark theme
- Normal text size
- Large text size
- Default Focus First method
- Suggested breaks on or off
- Reduce Motion
- Reset Preferences

App preferences are saved using browser `localStorage`, allowing them to remain active when the user refreshes the application or changes pages.

---

## Profile

The Profile section displays the user's:

- Name
- Email address

Users can:

- Edit their profile
- Change their password

Email addresses must remain unique between accounts.

---

## Account

Users can securely log out of their UltiPlan 365 account from Settings.

---

## Privacy & Data

UltiPlan 365 connects account information, tasks, and study preferences to the user's experience.

Task records are associated with individual user accounts so that one UltiPlan 365 user cannot access another user's tasks through the normal application interface.

---

## Delete Account

Users can permanently delete their UltiPlan 365 account.

Before deletion, the user must confirm the action using their current password.

Deleting an account removes:

- The user account
- Active tasks belonging to the user
- Completed tasks belonging to the user

Account deletion cannot be undone.

---

## About UltiPlan 365

The Settings page also includes basic application information and the current version.

**Current Version: 1.0**

---

# Priority Score System

UltiPlan 365 prioritizes tasks using three major factors:

1. Deadline
2. Importance
3. Difficulty

Points from these factors are combined to calculate the task's priority score.

Tasks with higher priority scores appear before lower-priority tasks.

This priority system is used throughout the application, including:

- Dashboard
- View Tasks
- Study Planner
- Focus First

---

# Multi-User Data System

UltiPlan 365 was originally developed as a local task-planning MVP.

The application now supports multiple user accounts.

Each task contains a relationship to the user who created it.

When retrieving tasks, UltiPlan 365 filters the database using the currently authenticated user's account ID.

This means:

- User A sees User A's tasks
- User B sees User B's tasks
- Completing a task affects only its owner
- Deleting a task affects only its owner
- Study plans are generated from the current user's tasks
- Focus First selects from the current user's tasks

This allows multiple students to use the same application while maintaining separate task collections.

---

# Technologies Used

UltiPlan 365 uses:

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Login
- SQLite
- Werkzeug password hashing
- itsdangerous

### Frontend

- HTML
- CSS
- JavaScript
- Jinja templates
- Browser localStorage

### Email and Account Recovery

- Python `smtplib`
- `EmailMessage`
- Gmail SMTP
- Time-limited password-reset tokens

### Development

- Git
- GitHub
- GitHub Codespaces
- Environment variables
- GitHub Codespaces secrets

---

# Project Structure

```text
UltiPlan-365/
│
├── app.py
├── app_terminal.py
├── models.py
├── priority.py
├── storage.py
├── study_planner.py
├── task_logic.py
├── requirements.txt
├── README.md
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
    ├── settings.html
    ├── register.html
    ├── login.html
    ├── forgot_password.html
    ├── reset_password.html
    ├── reset_email_sent.html
    ├── edit_profile.html
    ├── change_password.html
    └── delete_account.html
```

The application's SQLite database is created within the application's local instance environment and is excluded from Git tracking.

---

# Database

UltiPlan 365 uses **SQLite with SQLAlchemy** to store application data.

The database contains user and task information.

## Users

User records contain account information required for authentication and personalization.

Passwords are not stored directly. Instead, password hashes are stored and checked during authentication.

## Tasks

Task records are associated with individual users through a user ID.

This relationship allows the application to retrieve only the tasks belonging to the currently authenticated student.

---

# Environment Variables

UltiPlan 365 uses environment variables for information that should not be hard-coded directly into the source code.

The password-reset system currently uses:

```text
ULTIPLAN_EMAIL
ULTIPLAN_EMAIL_PASSWORD
ULTIPLAN_BASE_URL
```

### `ULTIPLAN_EMAIL`

The email account used to send UltiPlan 365 password-reset messages.

### `ULTIPLAN_EMAIL_PASSWORD`

The application credential used by the email system.

### `ULTIPLAN_BASE_URL`

The public base address used when generating password-reset links.

For example, during development this can point to the application's forwarded development address. When the application is deployed, the value can be changed to the production domain without changing the password-reset code.

> Secret values should never be committed to the GitHub repository.

Development secrets are managed separately from the source code.

---

# How to Run the Application

## 1. Open the project directory

```bash
cd /workspaces/UltiPlan-365
```

## 2. Install the required packages

```bash
pip install -r requirements.txt
```

## 3. Configure required environment variables

The password-reset email system requires the appropriate environment variables to be available before starting the application.

Never place private credentials directly inside the README or commit them to GitHub.

## 4. Start Flask

```bash
python3 app.py
```

## 5. Open the application

Open the local or forwarded Flask address.

When using GitHub Codespaces, open the forwarded Flask port from the **Ports** section.

---

# How to Use UltiPlan 365

1. Register for an UltiPlan 365 account.
2. Log in using the registered email and password.
3. Add an academic task.
4. Enter the course, deadline, estimated time, importance, and difficulty.
5. Save the task.
6. Review prioritized tasks from the Dashboard or View Tasks.
7. Use Study Planner when you have a specific amount of study time available.
8. Use Focus First to identify and begin the highest-priority task.
9. Use the focus timer while studying.
10. Use Task Manager to complete, restore, or delete tasks.
11. Use Settings to customize study preferences and manage the account.
12. Log out when finished.

---

# Input Validation

UltiPlan 365 checks user input before saving important information.

Task validation includes:

- Blank task names
- Blank course names
- Invalid deadlines
- Deadlines in the past
- Invalid estimated time
- Estimated time less than or equal to zero

Account-related validation includes:

- Duplicate email addresses
- Incorrect passwords
- New-password confirmation
- Minimum password length
- Password-reset token expiration

When invalid information is entered, the application provides feedback explaining what needs to be corrected.

---

# Security and Account Protection

UltiPlan 365 includes several account-protection measures.

These include:

- Password hashing
- Login-protected application routes
- User-specific database queries
- Unique account email addresses
- Password verification before account deletion
- Time-limited password-reset tokens
- Password-reset token expiration after 30 minutes
- Environment variables for email credentials and application URLs
- Generic forgot-password responses that do not reveal whether an email address is registered

These measures help separate user accounts and avoid exposing sensitive credentials directly in the source code.

---

# Current Project Status

UltiPlan 365 currently includes the core functionality required for students to create an account and manage their study workload.

Completed systems include:

- User registration
- User login and logout
- User-specific task storage
- Profile editing
- Password changes
- Forgot Password
- Email password recovery
- Time-limited reset links
- Account deletion
- Task creation
- Task input validation
- Priority-score calculation
- Priority sorting
- Dashboard workload overview
- Active-task viewing
- Task search
- Study-plan generation
- Focus First recommendation
- Multiple focus-session methods
- Focus timer
- Suggested breaks
- Task completion
- Task restoration
- Task deletion
- Progress tracking
- Theme preferences
- Text-size preferences
- Reduce Motion preference
- Browser-saved settings
- Privacy and account-management information

UltiPlan 365 has progressed beyond its original terminal and single-user MVP into a multi-user Flask web application.

---

# Future Improvements

Possible future improvements include:

- Editing existing tasks
- Deadline and reminder notifications
- Calendar integration
- Importing assignments
- Task notes and categories
- More detailed productivity analytics
- Mobile optimization
- Persistent focus-session progress
- Production cloud database
- Public production deployment

These additions are not required for the current version but could expand UltiPlan 365 in future releases.

---

# Challenges and Learning

Building UltiPlan 365 involved solving problems across both backend and frontend development.

Some of the major challenges included:

- Moving from a terminal application to a Flask web application
- Connecting Flask routes to HTML forms
- Building a task-priority system
- Generating study plans from available time
- Creating a JavaScript countdown timer
- Connecting focus sessions to estimated task time
- Tracking focus and break time separately
- Passing Python task data into JavaScript
- Saving interface preferences with `localStorage`
- Applying themes consistently across pages
- Building user registration and login
- Connecting tasks to individual user accounts
- Protecting routes with authentication
- Hashing and verifying passwords
- Preventing duplicate account emails
- Building profile and password-management pages
- Creating password-reset tokens
- Sending real password-reset emails
- Debugging development URLs inside emailed reset links
- Moving configuration values into environment variables
- Managing secrets through GitHub Codespaces
- Safely deleting a user and their associated tasks
- Maintaining consistent page design as the application grew
- Using Git and GitHub to preserve working checkpoints

Working through these challenges strengthened my understanding of:

- Python
- Flask
- SQLAlchemy
- Relational application data
- User authentication
- Password security
- HTML
- CSS
- JavaScript
- Jinja
- Email systems
- Environment variables
- Debugging
- Git
- GitHub
- Full-stack web application structure

---

# Author

**Moyinoluwa Ajibade**

Developer and creator of UltiPlan 365.

---

# Version

**UltiPlan 365**  
Version 1.0  
2026

© 2026 AMG. UltiPlan 365. All rights reserved.