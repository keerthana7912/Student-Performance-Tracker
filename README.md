# 🎓 Student Performance Tracker

## Overview
A Python + Flask application that lets teachers track student performance
across three subjects (Python, Java, MySQL). It's available in two forms
that share the same SQLite database:

- **`main.py`** — a menu-driven command-line version
- **`app.py`** — a full web version (add / edit / delete / search / dashboard)

## Features
- Add, edit, delete, and search students
- Automatic average + letter grade calculation
- Dashboard with charts (grade distribution, subject averages)
- Subject-wise topper lookup
- Class average (overall or per subject)
- Local text-file backup of all data (`backup.txt`)

## Technologies Used
- Python, Flask, SQLite (via `sqlite3`)
- HTML, CSS, JavaScript, Chart.js
- gunicorn (production server)

## Project Structure
```
student.py      -> Student class (OOP model)
tracker.py      -> StudentTracker class (CLI business logic)
database.py     -> All database access (shared by CLI and web app)
main.py         -> Command-line interface
app.py          -> Flask web application
templates/      -> HTML templates
static/         -> CSS
```

## How to Run Locally

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the **web app**:
   ```
   python app.py
   ```
   Then open http://127.0.0.1:5000

   Or run the **command-line version**:
   ```
   python main.py
   ```

## Usage Guide (Web App)

### 1. Add a student
- Go to **➕ Add Student** in the sidebar.
- Example: Name = `Asha Rao`, Roll Number = `101`, Python = `85`,
  Java = `78`, MySQL = `92`.
- Click **Add Student** — you'll be redirected to the student list,
  where the average (85.0) and grade (A) are calculated automatically.

### 2. View / edit / delete a student
- Go to **👨‍🎓 Students** to see every student in a table.
- Click **✏️ Edit** next to any row to update their marks.
- Click **🗑 Delete** to remove a student (with a confirmation prompt).

### 3. Search for a student
- Go to **🔍 Search**.
- Enter either a full/partial name (e.g. `Asha`) or an exact roll
  number (e.g. `101`) and click **Search**.

### 4. Find a subject's top performer (bonus)
- Go to **🏆 Topper**, choose a subject (Python / Java / MySQL), and
  submit — the highest-scoring student in that subject is shown.

### 5. View class-wide statistics
- Go to **📊 Dashboard** to see total students, overall class average,
  the top and lowest performer, a grade-distribution pie chart, and a
  per-subject average bar chart.

### 6. Back up your data
- Click **💾 Backup** at any time to download `backup.txt`, a plain-text
  snapshot of every student's marks. A backup is also refreshed
  automatically on every add/edit/delete.

## Usage Guide (Command-Line App)
Run `python main.py` and follow the on-screen menu:
```
1. Add Student
2. Add Grades (Python/Java/MySQL)
3. View Student Details
4. Calculate Average
5. Display All Students
6. Subject-Wise Topper
7. Class Average
8. Backup Data to File
9. Exit
```
Example flow: choose `1` to add a student, `2` to record their Python
mark, then `3` to view their full report.

## Deployment
The app is ready for deployment to Heroku (or any Heroku-compatible
platform such as Render):

- `requirements.txt` lists the dependencies (Flask, gunicorn).
- `Procfile` starts the app with `gunicorn app:app`.

**Live app:** _add your deployed URL here after deploying._

## Developed By
Keerthana V
