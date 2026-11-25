# StudyFlow — Private Study Planner

StudyFlow is a multi-user Flask app for students to plan coursework and record focused study time. Each account has its own private tasks and study log.

## Features

- Private accounts with password hashing and login sessions
- CSRF protection for forms and sign-out
- Add, edit, complete, reopen, and delete study tasks
- Record subject, due date, and low/medium/high priority
- Filter all tasks, active tasks, overdue tasks, or completed tasks
- Search task names and subjects
- Dashboard totals for active, completed, overdue, and due-today tasks
- Weekly study-time summary and subject breakdown
- Log study sessions with duration, date, subject, and notes
- SQLite database is created automatically; PostgreSQL is supported through `DATABASE_URL`
- Responsive dark interface with no frontend build step
- Basic validation on the server

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

Open http://127.0.0.1:5000, choose **Create account**, then start adding tasks or logging sessions.

## Configuration

The app uses SQLite by default. Before deploying, set a strong random `SECRET_KEY` and an appropriate `DATABASE_URL`. Set `COOKIE_SECURE=1` when serving over HTTPS. Keep `FLASK_DEBUG` unset in production.

## Project layout

```text
studyflow-flask/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── edit.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── sessions.html
└── static/
    └── style.css
```

## Production checklist

This is a portfolio and learning app foundation. Before real public use, add account email verification and password reset, database migrations and backups, rate limiting, a production WSGI server, HTTPS, monitoring, and a privacy policy. Do not use Flask's debug server on a public network. Set a strong secret key outside the source code.


