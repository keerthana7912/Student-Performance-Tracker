class Student:
    """
    Represents a single student and their marks.
    Used by both the CLI app (tracker.py) and the Flask web app (app.py)
    so the OOP design is shared, not duplicated.
    """

    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.grades = {}  # e.g. {"python": 90, "java": 85, "mysql": 78}

    def add_grade(self, subject, grade):
        """
        Add or update a grade for a subject.
        """
        self.grades[subject.lower()] = grade

    def calculate_average(self):
        """
        Calculate the average grade of the student.
        Returns 0 if no grades are available.
        """
        if not self.grades:
            return 0

        total = sum(self.grades.values())
        average = total / len(self.grades)
        return round(average, 2)

    def letter_grade(self):
        """
        Convert the numeric average into a letter grade (A+, A, B, C, D).
        """
        average = self.calculate_average()

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

    def display_information(self):
        """
        Display complete student information.
        """
        print("\n========== Student Details ==========")
        print(f"Name         : {self.name}")
        print(f"Roll Number  : {self.roll_number}")

        if self.grades:
            print("\nGrades:")
            for subject, grade in self.grades.items():
                print(f"{subject.title()} : {grade}")
        else:
            print("\nNo grades available.")

        print(f"\nAverage Grade : {self.calculate_average():.2f}")
        print(f"Letter Grade  : {self.letter_grade()}")
        print("=====================================\n")

    @classmethod
    def from_db_row(cls, row):
        """
        Build a Student object from a sqlite3.Row returned by database.py.
        """
        student = cls(row["name"], row["roll_number"])

        for subject in ("python", "java", "mysql"):
            if row[subject] is not None:
                student.add_grade(subject, row[subject])

        return student
