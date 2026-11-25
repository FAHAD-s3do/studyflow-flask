# StudyFlow — Flask Study Planner

A small, polished study planner built with Flask and SQLite. Add assignments or study sessions, set subjects and due dates, choose priorities, search tasks, filter by status, and mark work complete.

## Features

- Create and delete study tasks
- Track subject, due date, and priority
- Filter active and completed tasks
- Search by title or subject
- Dashboard counts, including overdue tasks
- SQLite database created automatically
- Responsive interface with no frontend build step

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
```

Activate the environment:

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
│   └── index.html
└── static/
    └── style.css
```

## What this project demonstrates

Flask routes and form handling, Jinja templates, SQLAlchemy models and queries, SQLite persistence, flash messages, search and filters, and basic input validation.

## Before deploying publicly

Set a strong `SECRET_KEY` through an environment variable, turn off debug mode, and run Flask behind a production WSGI server such as Gunicorn. Add authentication and CSRF protection before allowing multiple users to manage private data.

