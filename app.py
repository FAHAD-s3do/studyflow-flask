import os
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import case, func

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "studyflow-local-dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studyflow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(60), nullable=False, default="General")
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default="medium")
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    @property
    def overdue(self):
        return not self.completed and self.due_date is not None and self.due_date < date.today()


def task_form_data():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "General").strip() or "General"
    due_value = request.form.get("due_date", "").strip()
    priority = request.form.get("priority", "medium")
    if not title:
        return None, "Add a task title first."
    if len(title) > 120 or len(subject) > 60:
        return None, "Title must be under 120 characters and subject under 60."
    if priority not in {"low", "medium", "high"}:
        return None, "Choose a valid priority."
    try:
        due_date = date.fromisoformat(due_value) if due_value else None
    except ValueError:
        return None, "Enter a valid due date."
    return {"title": title, "subject": subject, "due_date": due_date, "priority": priority}, None


@app.get("/")
def index():
    status = request.args.get("status", "all")
    if status not in {"all", "active", "overdue", "completed"}:
        status = "all"
    search = request.args.get("q", "").strip()
    query = Task.query
    if status == "active":
        query = query.filter_by(completed=False)
    elif status == "overdue":
        query = query.filter(Task.completed.is_(False), Task.due_date < date.today())
    elif status == "completed":
        query = query.filter_by(completed=True)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%") | Task.subject.ilike(f"%{search}%"))
    priority_order = case((Task.priority == "high", 0), (Task.priority == "medium", 1), else_=2)
    tasks = query.order_by(Task.completed.asc(), Task.due_date.is_(None), Task.due_date.asc(), priority_order).all()
    total = Task.query.count()
    done = Task.query.filter_by(completed=True).count()
    active = total - done
    overdue = Task.query.filter(Task.completed.is_(False), Task.due_date < date.today()).count()
    due_today = Task.query.filter_by(completed=False, due_date=date.today()).count()
    progress = round(done / total * 100) if total else 0
    return render_template("index.html", tasks=tasks, status=status, search=search,
                           total=total, done=done, active=active, overdue=overdue,
                           due_today=due_today, progress=progress)


@app.post("/tasks")
def create_task():
    data, error = task_form_data()
    if error:
        flash(error, "error")
        return redirect(url_for("index"))
    db.session.add(Task(**data))
    db.session.commit()
    flash("Task added to your study plan.", "success")
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    if request.method == "POST":
        data, error = task_form_data()
        if error:
            flash(error, "error")
            return render_template("edit.html", task=task)
        for key, value in data.items():
            setattr(task, key, value)
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("index", status="all"))
    return render_template("edit.html", task=task)


@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    task = db.get_or_404(Task, task_id)
    task.completed = not task.completed
    db.session.commit()
    flash("Task marked complete." if task.completed else "Task moved back to your plan.", "success")
    return redirect(request.referrer or url_for("index"))


@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

