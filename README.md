# StudyFlow — Flask Study Planner

A dark, responsive study planner built with Flask and SQLite. Organize coursework, keep deadlines visible, and track your progress in one place.

## Features

- Add, edit, complete, reopen, and delete study tasks
- Record a subject, due date, and low/medium/high priority
- Filter all tasks, active tasks, overdue tasks, or completed tasks
- Search task names and subjects
- Dashboard totals for all, active, completed, overdue, and due today
- Completion progress ring
- SQLite database is created automatically
- Responsive black interface with no frontend build step
- Basic server-side form validation

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
```

Activate the environment:

- Windows Command Prompt: `.venv\Scripts\activate.bat`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Install packages and start the app:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Project layout

```text
studyflow-flask/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── edit.html
│   └── index.html
└── static/
    └── style.css
```

## What this project demonstrates

Flask routes, Jinja templates, form handling and validation, SQLAlchemy models and queries, SQLite persistence, flash messages, filtering, search, and CRUD operations.

## Before deploying publicly

Set a strong `SECRET_KEY` environment variable, turn off debug mode, and run Flask behind a production WSGI server such as Gunicorn. Add authentication and CSRF protection before allowing multiple users to manage private data.

