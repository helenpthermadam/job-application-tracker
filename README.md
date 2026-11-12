# Job Application Tracker

A Django web app to track job applications from "Saved" to "Offer". Each user has a private account and only sees their own applications.

> **Status:** In progress. Core features work; more are planned (see Roadmap).

## Features

- User sign up, log in and log out (Django authentication)
- Add, view, edit and delete job applications (CRUD)
- Status tracking: Saved, Applied, Interview, Offer, Rejected
- Dashboard with a count per status
- Search by company, role or location, and filter by status
- Follow-up dates, with overdue ones highlighted
- Pagination and a responsive Bootstrap 5 interface
- Customised Django admin (filters, search, date drill-down)
- Unit tests (models, auth, CRUD, privacy, search and filter)

## Tech stack

Python, Django, SQLite (MySQL planned), HTML, Bootstrap 5, Git/GitHub

## Run it locally

```bash
# 1. Clone and enter the project
git clone https://github.com/helenpthermadam/job-application-tracker.git
cd job-application-tracker

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database tables
python manage.py migrate

# 5. (Optional) create an admin user for /admin/
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign up for an account.

## Run the tests

```bash
python manage.py test
```

## Project structure

```
config/          Project settings and root URLs
applications/    The main app
  models.py      JobApplication model
  forms.py       Application form and sign-up form
  views.py       Dashboard, CRUD views and sign-up
  urls.py        App routes
  admin.py       Admin customisation
  tests.py       Unit tests
templates/       HTML templates (base, applications, registration)
```

## Roadmap

- [ ] REST API with Django REST Framework
- [ ] Export applications to CSV
- [ ] Management command that lists today's follow-ups
- [ ] Switch to MySQL, with settings read from environment variables
- [ ] Deploy a live demo

## Configuration

Settings read these environment variables (see `.env.example`): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`. The defaults are for local development only.

## Author

Helen P Thermadam
