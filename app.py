from flask import Flask, render_template, request, redirect, send_file
import sqlite3

import database
from student import Student

app = Flask(__name__)

# Table is created automatically when database.py is imported.


# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Add Student
# ==========================

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        roll_number = int(request.form["roll_number"])
        python_mark = int(request.form["python"])
        java_mark = int(request.form["java"])
        mysql_mark = int(request.form["mysql"])

        if not all(is_valid_mark(m) for m in (python_mark, java_mark, mysql_mark)):
            return "Marks should be between 0 and 100"

        try:
            database.insert_student(roll_number, name, python_mark, java_mark, mysql_mark)
        except sqlite3.IntegrityError:
            return "Roll Number already exists"

        database.backup_to_file()  # keep the local backup file current

        return redirect("/students")

    return render_template("add_student.html")


# ==========================
# View Students
# ==========================

@app.route("/students")
def students():
    rows = database.get_all_students()
    return render_template("students.html", students=rows)


# ==========================
# Search Student
# ==========================

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []

    if request.method == "POST":
        keyword = request.form["keyword"]
        results = database.search_students(keyword)

    return render_template("search.html", students=results)


# ==========================
# Edit Student
# ==========================

@app.route("/edit/<int:roll_number>", methods=["GET", "POST"])
def edit_student(roll_number):

    if request.method == "POST":
        name = request.form["name"]
        python_mark = int(request.form["python"])
        java_mark = int(request.form["java"])
        mysql_mark = int(request.form["mysql"])

        if not all(is_valid_mark(m) for m in (python_mark, java_mark, mysql_mark)):
            return "Marks should be between 0 and 100"

        database.update_student(roll_number, name, python_mark, java_mark, mysql_mark)
        database.backup_to_file()

        return redirect("/students")

    student = database.get_student(roll_number)

    if not student:
        return "Student not found"

    return render_template("edit_student.html", student=student)


# ==========================
# Delete Student
# ==========================

@app.route("/delete/<int:roll_number>")
def delete_student(roll_number):
    database.delete_student(roll_number)
    database.backup_to_file()
    return redirect("/students")


# ==========================
# Subject-Wise Topper (bonus)
# ==========================

@app.route("/topper", methods=["GET", "POST"])
def topper():
    result = None
    subject = None

    if request.method == "POST":
        subject = request.form["subject"].lower()
        result = database.get_subject_topper(subject)

    return render_template("topper.html", topper=result, subject=subject)


# ==========================
# Backup (deliverable)
# ==========================

@app.route("/backup")
def backup():
    path = database.backup_to_file()
    return send_file(path, as_attachment=True)


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    rows = database.get_all_students()
    total_students = len(rows)

    class_average = database.get_class_average()

    top_student = None
    lowest_student = None
    if rows:
        top_student = max(rows, key=lambda r: r["average"] or 0)
        lowest_student = min(rows, key=lambda r: r["average"] or 0)

    grade_counts_map = {}
    for row in rows:
        grade_counts_map[row["grade"]] = grade_counts_map.get(row["grade"], 0) + 1

    grades = list(grade_counts_map.keys())
    grade_counts = list(grade_counts_map.values())

    subject_average = {
        "python": database.get_class_average("python"),
        "java": database.get_class_average("java"),
        "mysql": database.get_class_average("mysql"),
    }

    return render_template(
        "dashboard.html",
        total_students=total_students,
        class_average=class_average,
        top_student=top_student,
        lowest_student=lowest_student,
        grades=grades,
        grade_counts=grade_counts,
        subject_average=subject_average
    )


# ==========================
# Helpers
# ==========================

def is_valid_mark(mark):
    """
    Helper function: validate that a mark is between 0 and 100.
    """
    return 0 <= mark <= 100


# ==========================
# Run Application
# ==========================

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
