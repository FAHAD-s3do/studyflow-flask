<div align="center">

# StudyFlow

### A focused, private study planner for students

Plan coursework, manage deadlines, and keep track of focused study time in one calm workspace.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-D71F00)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://sqlite.org/)

</div>

---

## Overview

StudyFlow is a multi-user Flask application for students who want a clear view of what to study next. Each student creates an account and gets a private planner, task list, and study log.

## What you can do

- **Plan coursework:** create, edit, complete, reopen, and remove tasks.
- **Set priorities and deadlines:** organize work by subject, due date, and priority.
- **Find the next task:** filter active, overdue, and completed work, or search by title and subject.
- **See progress:** view completion progress, due-today and overdue counts, and weekly study time.
- **Log study sessions:** record the subject, date, duration, and optional notes; review time by subject.
- **Keep accounts separate:** task and study-session queries are scoped to the signed-in student.

## Screens at a glance

The app uses a responsive dark interface with a personal dashboard, task planner, account pages, and a study-session log. Start it locally to explore the current UI.

## Tech stack

| Layer | Technology |
| --- | --- |
| Web app | Python, Flask |
| Database access | Flask-SQLAlchemy / SQLAlchemy |
| Local database | SQLite |
| PostgreSQL driver | Psycopg 3 |
| Authentication | Flask-Login, Werkzeug password hashing |
| Form protection | Flask-WTF CSRF protection |
| UI | Jinja templates, responsive CSS |

## Run locally

### Requirements

- Python 3.10 or newer
- Windows, macOS, or Linux

### Windows Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**, choose **Create account**, and start planning.

## Configuration

SQLite is used by default and the database is created automatically. For a hosted deployment, configure environment variables before starting the app:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Long, random value used to sign sessions and CSRF tokens |
| `DATABASE_URL` | Optional SQLAlchemy database URL; PostgreSQL is supported |
| `COOKIE_SECURE` | Set to `1` when the app is served over HTTPS |
| `FLASK_DEBUG` | Leave unset in production; set to `1` only for local debugging |

Example PowerShell session configuration:

```powershell
$env:SECRET_KEY = "replace-this-with-a-long-random-value"
$env:COOKIE_SECURE = "0"
python app.py
```

Never commit a real secret key or production database credentials.

## Project structure

```text
studyflow-flask/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── edit.html
    ├── index.html
    ├── login.html
    ├── register.html
    └── sessions.html
```

## Security and production readiness

The app hashes passwords, protects POST forms with CSRF tokens, uses HTTP-only / SameSite session cookies, and filters student records by account. The built-in server is for local learning only.

Before inviting students to a public deployment, add email verification and password reset, database migrations and backups, rate limiting, error monitoring, and a production WSGI server behind HTTPS. Set a stable `SECRET_KEY` and a production database URL in the hosting environment. Review privacy and retention requirements for your intended audience.

## Next steps

- Add password reset and email verification
- Add database migrations and backup automation
- Add automated checks in CI
- Deploy a hosted demo with HTTPS

