from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

#Creates the database object
db = SQLAlchemy()

#Stores each UltiPlan user
class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(225),
        nullable=False
    )

#Storing each task created by a user
class Task(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    #Connecting this task to the user who created it
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    task_name = db.Column(
        db.String(200),
        nullable=False
    )

    course = db.Column(
        db.String(150),
        nullable=False
    )

    deadline = db.Column(
        db.String(20),
        nullable=False
    )

    importance = db.Column(
        db.String(20),
        nullable=False
    )

    difficulty = db.Column(
        db.String(20),
        nullable=False
    )

    estimated_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    priority_score = db.Column(
        db.Integer,
        default=0
    )
    
    completed = db.Column(
        db.Boolean,
        default=False
    )