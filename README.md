<div align="center">

# StudyFlow

### Plan with clarity. Study with intention.

A private, multi-user study planner built with **Python, Flask, and SQLAlchemy**. Organize coursework, stay ahead of deadlines, and turn focused study sessions into visible progress.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-111827?style=for-the-badge&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**A calm workspace for consistent progress.**

</div>

---

## Overview

StudyFlow gives each student a personal workspace to manage academic tasks and record focused study time. The dashboard brings deadlines, priorities, completion progress, and weekly study activity into one responsive interface.

## Product highlights

| Area | Capabilities |
| --- | --- |
| Task planning | Create, edit, complete, reopen, and delete coursework tasks |
| Prioritization | Organize work by subject, due date, and priority |
| Task discovery | Filter active, overdue, and completed tasks; search by title or subject |
| Progress dashboard | Track completion rate, active tasks, overdue work, and tasks due today |
| Study journal | Log duration, subject, date, and optional notes |
| Time insights | Review weekly focus time and time grouped by subject |
| Private accounts | Keep each student's tasks and sessions scoped to their account |

## Interface & experience

- Responsive dark interface for desktop and mobile.
- Subtle entrance transitions across dashboard sections and cards.
- Gentle ambient background motion and progress-ring animation.
- Interactive hover feedback for cards, task rows, and controls.
- Reduced-motion support for accessibility.
- CSS-based animation; no front-end animation framework required.

## Technology

| Layer | Stack |
| --- | --- |
| Application | Python 3.10+, Flask 3.1 |
| Data layer | Flask-SQLAlchemy / SQLAlchemy |
| Database | SQLite by default; PostgreSQL supported |
| Authentication | Flask-Login, Werkzeug password hashing |
| Form security | Flask-WTF CSRF protection |
| Rendering | Jinja2 templates |
| Styling | Responsive CSS, CSS keyframe animations |

## Getting started

### Prerequisites
- Python 3.10 or newer
- Git
- Windows, macOS, or Linux

### 1. Clone the repository
```bash
git clone https://github.com/FAHAD-s3do/studyflow-flask.git
cd studyflow-flask
```

### 2. Create and activate a virtual environment

**Windows — Command Prompt**
```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure and run

**PowerShell**
```powershell
$env:SECRET_KEY = "replace-with-a-long-random-secret"
$env:COOKIE_SECURE = "0"
python app.py
```

**macOS / Linux**
```bash
export SECRET_KEY="replace-with-a-long-random-secret"
export COOKIE_SECURE="0"
python app.py
```

Open **http://127.0.0.1:5000** and create your account.

> The Flask development server is for local development only. Use a production WSGI server and HTTPS for deployment.

## Project structure

```text
studyflow-flask/
├── app.py                  # Flask routes, models, and setup
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css           # Responsive UI and motion system
└── templates/
    ├── base.html           # Shared layout and navigation
    ├── index.html          # Study planner dashboard
    ├── sessions.html       # Study log and weekly insights
    ├── edit.html           # Task editing
    ├── login.html          # Sign in
    └── register.html       # Account creation
```

## Configuration

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Secret used to sign sessions and CSRF tokens |
| `DATABASE_URL` | Optional SQLAlchemy database URL; PostgreSQL is supported |
| `COOKIE_SECURE` | Set to `1` when served over HTTPS |
| `FLASK_DEBUG` | Set to `1` only for local debugging |

Never commit real secrets, credentials, or production database URLs.

## Security notes

The application uses password hashing, CSRF protection for forms, HTTP-only and SameSite session cookies, and account-scoped task and study-session queries.

Before a public production launch, consider adding:
- Email verification and secure password-reset flows.
- Database migrations, automated backups, and restore testing.
- Login and form rate limiting.
- Security headers, centralized error handling, and monitoring.
- A production WSGI server behind HTTPS.
- A documented privacy and data-retention policy.

## Roadmap

- [ ] Add automated tests for authentication and task workflows.
- [ ] Add database migrations.
- [ ] Add password reset and email verification.
- [ ] Add CI checks and deployment workflow.
- [ ] Publish a hosted demo and real application screenshots.

---

<div align="center">

**StudyFlow** · Built for focus, one task at a time.

</div>
