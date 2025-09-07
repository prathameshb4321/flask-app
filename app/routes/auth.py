# ---------- Auth Routes (demo only) ----------
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

USER_CREDENTIALS = {"username": "admin", "password": "1234"}

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
            session["user"] = username
            flash("Logged in successfully.", "success")
            return redirect(url_for("tasks.list_tasks"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
