from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash

from task_logic import create_task
from study_planner import create_study_plan

from models import db, User, Task
from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)

from itsdangerous import URLSafeTimedSerializer

import os 
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

#Flask needs a secret key to display temporary messages
app.secret_key = "ultiplan365-secret-key"

#Used to create secure, temporary password reset links
serializer = URLSafeTimedSerializer(app.secret_key)

#Email account used to send password reset links
ULTIPLAN_EMAIL = os.environ.get("ULTIPLAN_EMAIL")
ULTIPLAN_EMAIL_PASSWORD = os.environ.get("ULTIPLAN_EMAIL_PASSWORD")

#Datatbase configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ultiplan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Connecting SQLAlchemy to this Flask app
db.init_app(app)

# Setting up flask-login
login_manager = LoginManager()
login_manager.init_app(app)

#If someone tries to open a protected page without logging in,
#Flask-login will send them to the login page
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

#Sending a password reset email
def send_reset_email(user_email, reset_link):
    message = EmailMessage()

    message["Subject"] = "UltiPlan 365 Password Reset "
    message["From"] = ULTIPLAN_EMAIL
    message["To"] = user_email

    message.set_content(
        f"""Hello,
You requested to reset your UltiPlan 365 password.
Use the link below to create a new password:
{reset_link}
This link will expire in 30 minutes.
If you did not request this, you can ignore this email.

Thank you,
UltiPlan 365
"""
    )
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(
            ULTIPLAN_EMAIL,
            ULTIPLAN_EMAIL_PASSWORD
        )

        server.send_message(message)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #Getting the info entered in the registration form
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        #Making sure all fields were completed
        if not name or not email or not password:
            return render_template(
                "register.html",
                error="Please complete all fields."
            )
        
        #Checking if an account already uses this email
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template(
                "register.html",
                error="An account with this email already exists."
            )
        
        #Turning the password into a secure password hash
        hashed_password = generate_password_hash(password)

        #Creating the new user
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password
        )

        #Saving the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!")

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        #Finding the user by email
        user = User.query.filter_by(email=email).first()

        #Checking that the user exists and the password matches
        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            flash("Login successful!")

            return redirect(url_for("home"))
        return render_template(
            "login.html",
            error="Invalid email or password."
        )
    return render_template("login.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":
        email = request.form["email"].strip().lower()

        #Looking for a user with this email
        user = User.query.filter_by(email=email).first()

        #If the account exists, create and email a secure reset link
        if user:
            token = serializer.dumps(
                user.email,
                salt="password-reset"
            )

            reset_link = (
                "https://legendary-giggle-697w96jp4jqf47g5-5000.app.github.dev"
                + url_for("reset_password", token=token)
            )

            try:
                send_reset_email(
                    user.email,
                    reset_link
                )
            except Exception as error:
                pass
                
        #Always showing the same message whether the email exists or not
        flash(
            "If an account exists with that email, a reset link will be sent."
        )
        
        return redirect(url_for("login"))
    return render_template("forgot_password.html")

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        #Reading the email stored inside the token
        #The link expires after 30 minutes
        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=1800
        )
    except Exception:
        flash("This password reset link is invalid or has expired.")
        return redirect(url_for("forgot_password"))
    
    #Finding the user connected to the email inside the token
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("This password reset link is invalid.")
        return redirect(url_for("forgot_password"))
    
    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
    
        #Making sure both password entries match
        if new_password != confirm_password:
            return render_template(
                "reset_password.html",
                error="The passwords do not match."
            )
        
        #Requiring at least 8 characters
        if len(new_password) < 8:
            return render_template(
                "reset_password.html",
                error="Your password must be at least 8 characters."
            )
        
        #Creating and saving the new password hash
        user.password_hash = generate_password_hash(
            new_password
        )

        db.session.commit()

        flash("Your password has been reset successfully.")

        return redirect(url_for("login"))
    return render_template("reset_password.html")


#Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash("You have been logged out.")
    return redirect(url_for("login"))

#Calculate the percentage of completed tasks
def calculate_daily_progress():
    #Counting this user's active tasks
    active_count = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).count()
    
    #Counting this user's completed tasks
    completed_count = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()

    total_tasks = active_count + completed_count

    if total_tasks == 0:
        return 0
    
    return round(
        completed_count / total_tasks * 100
    )

@app.route("/")
@login_required
def home():
    #Loading only the logges-in user's tasks
    active_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Task.priority_score.desc(),
        Task.deadline.asc()
    ).all()

    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).all()

    active_count = len(active_tasks)
    completed_count = len(completed_tasks)
    total_count = active_count + completed_count

    #Counting high priority active tasks
    high_priority_count = 0

    for task in active_tasks:
        if task.importance == "High":
            high_priority_count += 1
    
    #First task becomes Focus First recommendation
    focus_task = active_tasks[0] if active_tasks else None

    #Showing only first four tasks
    dashboard_tasks = active_tasks[:4]

    #Calculating the total estimated time for active tasks
    total_estimated_minutes = 0

    for task in active_tasks:
        total_estimated_minutes += task.estimated_minutes
    
    #Calculating the average priority score
    if active_tasks:
        total_priority_score = 0

        for task in active_tasks:
            total_priority_score += task.priority_score
        
        average_priority_score = round(
            total_priority_score / len(active_tasks)
        )
    else:
        average_priority_score = 0
    
    #Finding task with the nearest deadline
    if active_tasks:
        next_deadline_task = min(active_tasks, key=lambda task: task.deadline)
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
        next_deadline_task=next_deadline_task,
    )

@app.route("/add-task", methods=["GET", "POST"])
@login_required
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

        #Creating a database task for the logged-in user
        new_task = Task(
            user_id=current_user.id,
            course=task["course"],
            task_name=task["task_name"],
            deadline=task["deadline"],
            importance=task["importance"],
            difficulty=task["difficulty"],
            estimated_minutes=task["estimated_minutes"],
            priority_score=task["priority_score"],
            completed=False
        )

        #Saving the task to the database
        db.session.add(new_task)
        db.session.commit()        

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
@login_required
def view_tasks():
    #Loading only the logged-in user's active tasks
    tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Task.priority_score.desc(),
        Task.deadline.asc()
    ).all()

    return render_template(
        "view_tasks.html",
        tasks=tasks
    )

#Opening the Study Planner Page and processing available study time
@app.route("/study-planner", methods=["GET", "POST"])
@login_required
def study_planner():
    # Loading only the logged-in user's active tasks
    database_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Task.priority_score.desc(),
        Task.deadline.asc()
    ).all()

    #Converting database Task objects into dictionaries
    #so the original Study Planner logic can still use them
    tasks = []

    for task in database_tasks:
        tasks.append({
            "course": task.course,
            "task_name": task.task_name,
            "deadline": task.deadline,
            "importance": task.importance,
            "difficulty": task.difficulty,
            "estimated_minutes": task.estimated_minutes,
            "priority_score": task.priority_score
        })

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
@login_required
def focus_first():
    # Loading only the logged-in user's active tasks
    database_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Task.priority_score.desc(),
        Task.deadline.asc()
    ).all()

    #Converting database Task objects into dictionaries
    #because the Focus First JavaScript already expects task data
    tasks = []

    for task in database_tasks:
        tasks.append({
            "id": task.id,
            "course": task.course,
            "task_name": task.task_name,
            "deadline": task.deadline,
            "importance": task.importance,
            "difficulty": task.difficulty,
            "estimated_minutes": task.estimated_minutes,
            "priority_score": task.priority_score
        })

    # The first task is the highest-priority task
    focus_task = tasks[0] if tasks else None

    return render_template(
        "focus_first.html",
        focus_task=focus_task,
        tasks=tasks
    )

#Opening the page used to complete or delete tasks
@app.route("/task-manager")
@login_required
def task_manager():
    #Loading only this user's active tasks
    tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Task.priority_score.desc(),
        Task.deadline.asc()
    ).all()

    #Loading only this user's completed tasks
    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).order_by(
        Task.id.desc()
    ).all()

    return render_template(
        "task_manager.html", 
        tasks=tasks,
        completed_tasks=completed_tasks,
        active_count=len(tasks),
        completed_count=len(completed_tasks),
        total_count=len(tasks) + len(completed_tasks)
    )

@app.route("/complete-tasks/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    #Finding this task only if it belongs to the logged-in user
    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id,
        completed=False
    ).first_or_404()

    task.completed = True
    db.session.commit()
    flash("Task marked as completed!")

    return redirect(url_for("task_manager"))

@app.route("/delete-task/<int:task_id>", methods=["POST"])
@login_required
def delete_tasks(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id,
        completed=False
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully.")
    return redirect(url_for("task_manager"))

@app.route("/delete-completed-task/<int:task_id>", methods=["POST"])
@login_required
def delete_completed_task(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id,
        completed=True
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Completed task removed.")
    return redirect(url_for("task_manager"))

@app.route("/restore-completed-task/<int:task_id>", methods=["POST"])
@login_required
def restore_completed_task(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id,
        completed=True
    ).first_or_404()

    task.completed = False

    db.session.commit()

    flash("Task moved back to active tasks.")
    return redirect(url_for("task_manager"))

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()

        #Making sure another account is not already using this email
        existing_user = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if existing_user:
            flash("An account with this email already exists.")
            return redirect(url_for("edit_profile"))

        #Updating the logged-in user's information
        current_user.name = name
        current_user.email = email

        db.session.commit()

        flash("Your profile has been updated.")

        return redirect(url_for("settings"))
    return render_template("edit_profile.html")

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        #Checking that the current password is correct
        if not check_password_hash(
            current_user.password_hash,
            current_password
        ):
            return render_template(
                "change_password.html",
                error="Your current password is incorrect."
            )
        #Making sure the new passwords match
        if new_password != confirm_password:
            return render_template(
                "change_password.html",
                error="The new passwords do not match."
            )
        #Basic password length check
        if len(new_password) < 8:
            return render_template(
                "change_password.html",
                error="Your new password must be at least 8 characters."
            )
        #Preventing them from reusing the exact same password
        if check_password_hash(
            current_user.password_hash,
            new_password
        ):
            return render_template(
                "change_password.html",
                error="Your new password must be different from your current password."
            )
        # Hashing and saving the new password
        current_user.password_hash = generate_password_hash(
            new_password
        )
        db.session.commit()

        flash("Your password has been changed successfully.")

        return redirect(url_for("settings"))
    return render_template("change_password.html")

#Creating the database tables if they do not already exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )