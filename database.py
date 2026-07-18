import sqlite3

DB_NAME = "students.db"
SUBJECTS = ("python", "java", "mysql")


def connect_database():
    """
    Connect to SQLite database.
    If the database does not exist, it will be created automatically.
    """
    connection = sqlite3.connect(DB_NAME, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    """
    Create the students table if it does not already exist.
    Single shared schema used by BOTH the CLI app (main.py/tracker.py)
    and the Flask web app (app.py).
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            python INTEGER,
            java INTEGER,
            mysql INTEGER,
            average REAL,
            grade TEXT
        )
    """)

    connection.commit()
    connection.close()


def calculate_grade(average):
    """
    Convert a numeric average into a letter grade.
    """
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    else:
        return "D"


def insert_student(roll_number, name, python=None, java=None, mysql=None):
    """
    Insert a new student into the database.
    Raises sqlite3.IntegrityError if the roll number already exists.
    """
    average, grade = _compute_average_grade(python, java, mysql)

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (roll_number, name, python, java, mysql, average, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (roll_number, name, python, java, mysql, average, grade))

    connection.commit()
    connection.close()


def update_grades(roll_number, python, java, mysql):
    """
    Update a student's marks (and recompute average/grade).
    """
    average, grade = _compute_average_grade(python, java, mysql)

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET python=?, java=?, mysql=?, average=?, grade=?
        WHERE roll_number=?
    """, (python, java, mysql, average, grade, roll_number))

    connection.commit()
    connection.close()


def update_student(roll_number, name, python, java, mysql):
    """
    Update a student's name and marks (used by the web 'edit' route).
    """
    average, grade = _compute_average_grade(python, java, mysql)

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?, python=?, java=?, mysql=?, average=?, grade=?
        WHERE roll_number=?
    """, (name, python, java, mysql, average, grade, roll_number))

    connection.commit()
    connection.close()


def delete_student(roll_number):
    """
    Delete a student from the database.
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE roll_number=?", (roll_number,))

    connection.commit()
    connection.close()


def get_student(roll_number):
    """
    Retrieve a single student from the database.
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students WHERE roll_number=?", (roll_number,))
    student = cursor.fetchone()

    connection.close()
    return student


def get_all_students():
    """
    Retrieve all students from the database, ordered by roll number.
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students ORDER BY roll_number")
    students = cursor.fetchall()

    connection.close()
    return students


def search_students(keyword):
    """
    Search students by roll number (exact) or name (partial, case-insensitive).
    """
    connection = connect_database()
    cursor = connection.cursor()

    if keyword.isdigit():
        cursor.execute("SELECT * FROM students WHERE roll_number=?", (int(keyword),))
    else:
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{keyword}%",))

    students = cursor.fetchall()
    connection.close()
    return students


def get_subject_topper(subject):
    """
    Bonus feature: find the top-performing student in a given subject.
    """
    subject = subject.lower()
    if subject not in SUBJECTS:
        return None

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT * FROM students
        WHERE {subject} IS NOT NULL
        ORDER BY {subject} DESC
        LIMIT 1
    """)

    topper = cursor.fetchone()
    connection.close()
    return topper


def get_class_average(subject=None):
    """
    Bonus feature: class average, either overall or for one subject.
    """
    connection = connect_database()
    cursor = connection.cursor()

    if subject and subject.lower() in SUBJECTS:
        cursor.execute(f"SELECT AVG({subject.lower()}) AS avg_marks FROM students")
    else:
        cursor.execute("SELECT AVG(average) AS avg_marks FROM students")

    result = cursor.fetchone()
    connection.close()

    return round(result["avg_marks"], 2) if result and result["avg_marks"] is not None else 0


def backup_to_file(filename="backup.txt"):
    """
    Deliverable: save all student data locally to a text file as a backup.
    """
    students = get_all_students()

    with open(filename, "w") as f:
        f.write("========== STUDENT PERFORMANCE TRACKER — BACKUP ==========\n\n")

        if not students:
            f.write("No students available.\n")
        else:
            for s in students:
                f.write(f"Roll Number : {s['roll_number']}\n")
                f.write(f"Name        : {s['name']}\n")
                f.write(f"Python      : {s['python']}\n")
                f.write(f"Java        : {s['java']}\n")
                f.write(f"MySQL       : {s['mysql']}\n")
                f.write(f"Average     : {s['average']}\n")
                f.write(f"Grade       : {s['grade']}\n")
                f.write("-" * 40 + "\n")

    return filename


def _compute_average_grade(python, java, mysql):
    """
    Helper: compute average/grade from whichever marks are present.
    """
    marks = [m for m in (python, java, mysql) if m is not None]

    if not marks:
        return None, None

    average = round(sum(marks) / len(marks), 2)
    grade = calculate_grade(average)
    return average, grade


# Create the table automatically when this module is imported
create_table()
