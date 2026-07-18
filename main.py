from tracker import StudentTracker

tracker = StudentTracker()

while True:

    print("\n===================================")
    print("   STUDENT PERFORMANCE TRACKER")
    print("===================================")
    print("1. Add Student")
    print("2. Add Grades (Python/Java/MySQL)")
    print("3. View Student Details")
    print("4. Calculate Average")
    print("5. Display All Students")
    print("6. Subject-Wise Topper")
    print("7. Class Average")
    print("8. Backup Data to File")
    print("9. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        name = input("Enter Student Name: ")
        roll = int(input("Enter Roll Number: "))

        tracker.add_student(name, roll)

    elif choice == "2":

        roll = int(input("Enter Roll Number: "))
        subject = input("Enter Subject (Python/Java/MySQL): ")
        grade = int(input("Enter Grade: "))

        tracker.add_grades(roll, subject, grade)

    elif choice == "3":

        roll = int(input("Enter Roll Number: "))
        tracker.view_student_details(roll)

    elif choice == "4":

        roll = int(input("Enter Roll Number: "))
        tracker.calculate_average(roll)

    elif choice == "5":

        tracker.display_all_students()

    elif choice == "6":

        subject = input("Enter Subject (Python/Java/MySQL): ")
        tracker.subject_topper(subject)

    elif choice == "7":

        subject = input("Enter Subject (Python/Java/MySQL), or leave blank for overall: ")
        tracker.class_average(subject if subject.strip() else None)

    elif choice == "8":

        tracker.backup_to_file()

    elif choice == "9":

        print("Thank you for using Student Performance Tracker.")
        break

    else:

        print("Invalid choice.")
