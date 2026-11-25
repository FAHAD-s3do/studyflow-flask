import os
import re
import secrets
from datetime import date, timedelta

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import case, func, inspect, text
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
database_url = os.environ.get("DATABASE_URL", "sqlite:///studyflow.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("COOKIE_SECURE", "0") == "1"

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Log in to open your personal study space."
login_manager.login_message_category = "error"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    tasks = db.relationship("Task", backref="owner", lazy=True, cascade="all, delete-orphan")
    study_sessions = db.relationship("StudySession", backref="owner", lazy=True, cascade="all, delete-orphan")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)
    title = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(60), nullable=False, default="General")
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default="medium")
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    @property
    def overdue(self):
        return not self.completed and self.due_date is not None and self.due_date < date.today()


class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    subject = db.Column(db.String(60), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    session_date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if len(name) < 2 or len(name) > 60:
            flash("Name must be between 2 and 60 characters.", "error")
        elif not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            flash("Enter a valid email address.", "error")
        elif User.query.filter(func.lower(User.email) == email).first():
            flash("An account with that email already exists. Log in instead.", "error")
        elif len(password) < 10:
            flash("Use a password with at least 10 characters.", "error")
        elif password != confirm:
            flash("The passwords do not match.", "error")
        else:
            first_account = User.query.count() == 0
            user = User(name=name, email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.flush()
            if first_account:
                # Existing single-user demo tasks belong to the first account created.
                Task.query.filter_by(owner_id=None).update({Task.owner_id: user.id})
            db.session.commit()
            login_user(user)
            flash("Your private study space is ready.", "success")
            return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter(func.lower(User.email) == email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f"Welcome back, {user.name.split()[0]}.", "success")
            return redirect(url_for("index"))
        flash("Email or password is incorrect.", "error")
    return render_template("login.html")


@app.post("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "success")
    return redirect(url_for("login"))


@app.get("/")
@login_required
def index():
    status = request.args.get("status", "all")
    if status not in {"all", "active", "overdue", "completed"}:
        status = "all"
    search = request.args.get("q", "").strip()
    query = Task.query.filter_by(owner_id=current_user.id)
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
    owned = Task.query.filter_by(owner_id=current_user.id)
    total = owned.count()
    done = owned.filter_by(completed=True).count()
    active = total - done
    overdue = owned.filter(Task.completed.is_(False), Task.due_date < date.today()).count()
    due_today = owned.filter_by(completed=False, due_date=date.today()).count()
    progress = round(done / total * 100) if total else 0
    week_start = date.today() - timedelta(days=date.today().weekday())
    week_minutes = db.session.query(func.coalesce(func.sum(StudySession.duration_minutes), 0)).filter(
        StudySession.owner_id == current_user.id, StudySession.session_date >= week_start
    ).scalar()
    return render_template("index.html", tasks=tasks, status=status, search=search,
                           total=total, done=done, active=active, overdue=overdue,
                           due_today=due_today, progress=progress, week_minutes=week_minutes)


@app.post("/tasks")
@login_required
def create_task():
    data, error = task_form_data()
    if error:
        flash(error, "error")
        return redirect(url_for("index"))
    db.session.add(Task(owner_id=current_user.id, **data))
    db.session.commit()
    flash("Task added to your study plan.", "success")
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=current_user.id).first_or_404()
    if request.method == "POST":
        data, error = task_form_data()
        if error:
            flash(error, "error")
            return render_template("edit.html", task=task)
        for key, value in data.items():
            setattr(task, key, value)
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)


@app.post("/tasks/<int:task_id>/toggle")
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=current_user.id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    flash("Task marked complete." if task.completed else "Task moved back to your plan.", "success")
    return redirect(request.referrer or url_for("index"))


@app.post("/tasks/<int:task_id>/delete")
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.get("/sessions")
@login_required
def sessions():
    week_start = date.today() - timedelta(days=date.today().weekday())
    week_minutes = db.session.query(func.coalesce(func.sum(StudySession.duration_minutes), 0)).filter(
        StudySession.owner_id == current_user.id, StudySession.session_date >= week_start
    ).scalar()
    entries = StudySession.query.filter_by(owner_id=current_user.id).order_by(
        StudySession.session_date.desc(), StudySession.created_at.desc()
    ).limit(30).all()
    subjects = db.session.query(StudySession.subject, func.sum(StudySession.duration_minutes)).filter(
        StudySession.owner_id == current_user.id, StudySession.session_date >= week_start
    ).group_by(StudySession.subject).order_by(func.sum(StudySession.duration_minutes).desc()).all()
    return render_template("sessions.html", entries=entries, week_minutes=week_minutes, subjects=subjects, today=date.today().isoformat())


@app.post("/sessions")
@login_required
def log_session():
    subject = request.form.get("subject", "").strip()
    notes = request.form.get("notes", "").strip()
    raw_minutes = request.form.get("duration_minutes", "").strip()
    raw_date = request.form.get("session_date", "").strip()
    try:
        minutes = int(raw_minutes)
        session_date = date.fromisoformat(raw_date) if raw_date else date.today()
    except (ValueError, TypeError):
        flash("Enter a valid study duration and date.", "error")
        return redirect(url_for("sessions"))
    if not subject or len(subject) > 60 or len(notes) > 300 or not 1 <= minutes <= 600:
        flash("Add a subject, a note under 300 characters, and a duration from 1 to 600 minutes.", "error")
        return redirect(url_for("sessions"))
    db.session.add(StudySession(owner_id=current_user.id, subject=subject, duration_minutes=minutes,
                                 session_date=session_date, notes=notes or None))
    db.session.commit()
    flash("Study session logged. Nice work.", "success")
    return redirect(url_for("sessions"))


with app.app_context():
    db.create_all()
    # Keep older local SQLite demo databases usable after adding student accounts.
    if db.engine.dialect.name == "sqlite" and "owner_id" not in {column["name"] for column in inspect(db.engine).get_columns("task")}:
        with db.engine.begin() as connection:
            connection.execute(text("ALTER TABLE task ADD COLUMN owner_id INTEGER REFERENCES user(id)"))
            connection.execute(text("CREATE INDEX IF NOT EXISTS ix_task_owner_id ON task (owner_id)"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")






