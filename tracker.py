from student import Student
import database


VALID_SUBJECTS = ("python", "java", "mysql")


class StudentTracker:
    """
    Manages a collection of students, backed by the SQLite database.
    Uses the Student class for all in-memory representation/calculations,
    and database.py purely for persistence.
    """

    def add_student(self, name, roll_number):
        """
        Add a new student if the roll number is unique.
        """
        if database.get_student(roll_number):
            print("Student with this Roll Number already exists.")
            return

        student = Student(name, roll_number)
        database.insert_student(student.roll_number, student.name)
        print("Student added successfully.")

    def add_grades(self, roll_number, subject, grade):
        """
        Add/update a grade for a subject, validating input first.
        """
        if not is_valid_grade(grade):
            print("Grade should be between 0 and 100.")
            return

        subject = subject.lower()
        if subject not in VALID_SUBJECTS:
            print(f"Invalid Subject. Choose from: {', '.join(VALID_SUBJECTS)}")
            return

        row = database.get_student(roll_number)
        if not row:
            print("Student not found.")
            return

        student = Student.from_db_row(row)
        student.add_grade(subject, grade)

        database.update_grades(
            roll_number,
            student.grades.get("python"),
            student.grades.get("java"),
            student.grades.get("mysql"),
        )
        print("Grade added successfully.")

    def view_student_details(self, roll_number):
        """
        Display details of a student from the database.
        """
        row = database.get_student(roll_number)

        if not row:
            print("Student not found.")
            return

        student = Student.from_db_row(row)
        student.display_information()

    def calculate_average(self, roll_number):
        """
        Calculate and display the average grade for a student.
        """
        row = database.get_student(roll_number)

        if not row:
            print("Student not found.")
            return

        student = Student.from_db_row(row)

        if not student.grades:
            print("No grades available.")
            return

        print(f"Average Grade : {student.calculate_average():.2f} ({student.letter_grade()})")

    def display_all_students(self):
        """
        Display all students from the database.
        """
        rows = database.get_all_students()

        if not rows:
            print("No students available.")
            return

        print("\n========== Student List ==========")
        for row in rows:
            student = Student.from_db_row(row)
            print(f"Roll Number : {student.roll_number}")
            print(f"Name        : {student.name}")
            for subject in VALID_SUBJECTS:
                print(f"{subject.title():<10}: {student.grades.get(subject, '-')}")
            print(f"Average     : {student.calculate_average():.2f}")
            print("-" * 30)

    def subject_topper(self, subject):
        """
        Bonus: find the top-performing student in a subject.
        """
        row = database.get_subject_topper(subject)

        if not row:
            print("No data available for that subject.")
            return

        print(f"\nTop Student in {subject.title()}: {row['name']} "
              f"(Roll No. {row['roll_number']}) — {row[subject.lower()]} marks")

    def class_average(self, subject=None):
        """
        Bonus: class average, overall or for one subject.
        """
        avg = database.get_class_average(subject)
        label = subject.title() if subject else "Overall"
        print(f"\nClass Average ({label}): {avg}")

    def backup_to_file(self, filename="backup.txt"):
        """
        Deliverable: save all student data locally as a backup text file.
        """
        path = database.backup_to_file(filename)
        print(f"Backup saved to {path}")


def is_valid_grade(grade):
    """
    Helper function: validate that a grade is between 0 and 100.
    """
    return isinstance(grade, (int, float)) and 0 <= grade <= 100


def is_unique_roll_number(roll_number):
    """
    Helper function: check whether a roll number is not already in use.
    """
    return database.get_student(roll_number) is None
