# ---------- Task Routes ----------
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

@tasks_bp.route("/", methods=["GET"])
@login_required
def list_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("tasks.html", tasks=tasks)

@tasks_bp.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Title is required.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    if len(title) > 120:
        flash("Title too long (max 120 chars).", "danger")
        return redirect(url_for("tasks.list_tasks"))
    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    flash("Task added.", "success")
    return redirect(url_for("tasks.list_tasks"))

@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("tasks.list_tasks"))

@tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])
@login_required
def toggle_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.cycle_status()
    db.session.commit()
    flash(f"Status changed to {task.status}.", "success")
    return redirect(url_for("tasks.list_tasks"))
