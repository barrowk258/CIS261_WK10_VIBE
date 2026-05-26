# Kaitlin Barrow
# CIS261
# WK10 VIBE Coding
# Student Grade Calculator
# Data structure: Option A - list of dictionaries

import os
import sys

DATA_FILE = "student_grades.txt"


def get_single_keypress():
    """Read a single keypress from stdin without waiting for Enter."""
    try:
        import tty
        import termios
    except ImportError:
        return sys.stdin.read(1)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def load_records(filename):
    records = []
    if not os.path.exists(filename):
        return records

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Warning: Skipping malformed line {line_number} in {filename}.")
                    continue
                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    record = {
                        "name": name,
                        "id": student_id,
                        "test1": float(test1),
                        "test2": float(test2),
                        "test3": float(test3),
                        "average": float(average),
                        "grade": grade,
                    }
                except ValueError:
                    print(f"Warning: Invalid numeric data on line {line_number} in {filename}. Skipping.")
                    continue
                records.append(record)
    except OSError as error:
        print(f"Error loading records from {filename}: {error}")
    return records


def save_records(filename, records):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for record in records:
                line = "|".join([
                    record["name"],
                    record["id"],
                    f"{record['test1']:.2f}",
                    f"{record['test2']:.2f}",
                    f"{record['test3']:.2f}",
                    f"{record['average']:.2f}",
                    record["grade"],
                ])
                file.write(line + "\n")
        print(f"Saved {len(records)} student record(s) to {filename}.")
    except OSError as error:
        print(f"Error saving records to {filename}: {error}")


def calculate_average(test1, test2, test3):
    return (test1 + test2 + test3) / 3.0


def calculate_letter_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def format_score(score):
    return f"{score:.2f}"


def get_nonempty_string(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Please enter a non-empty value.")


def get_float(prompt_text):
    while True:
        value = input(prompt_text).strip()
        try:
            score = float(value)
            if 0.0 <= score <= 100.0:
                return score
            print("Score must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric score.")


def add_student(records):
    print("\nAdd New Student Record")
    name = get_nonempty_string("Student name: ")
    student_id = get_nonempty_string("Student ID: ")
    test1 = get_float("Test 1 score: ")
    test2 = get_float("Test 2 score: ")
    test3 = get_float("Test 3 score: ")
    average = calculate_average(test1, test2, test3)
    grade = calculate_letter_grade(average)
    records.append({
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    })
    print(f"Added {name} with average {format_score(average)} and grade {grade}.\n")


def display_students(records):
    if not records:
        print("No student records available.\n")
        return

    print("\nStudent Records")
    header = f"{'Name':<20} {'ID':<12} {'Test 1':>7} {'Test 2':>7} {'Test 3':>7} {'Avg':>7} {'Grade':>7}"
    print(header)
    print("-" * len(header))
    for record in records:
        print(
            f"{record['name']:<20} {record['id']:<12} "
            f"{format_score(record['test1']):>7} {format_score(record['test2']):>7} "
            f"{format_score(record['test3']):>7} {format_score(record['average']):>7} {record['grade']:>7}"
        )
    print()


def display_statistics(records):
    if not records:
        print("No student records available to calculate statistics.\n")
        return

    averages = [record["average"] for record in records]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print(f"Highest average: {format_score(highest)}")
    print(f"Lowest average:  {format_score(lowest)}")
    print(f"Class average:   {format_score(class_average)}\n")


def search_by_name(records):
    if not records:
        print("No student records available.\n")
        return

    search_name = input("Enter student name to search: ").strip().lower()
    if not search_name:
        print("Please enter a name to search.\n")
        return

    matches = [record for record in records if search_name in record["name"].lower()]
    if not matches:
        print(f"No students found matching '{search_name}'.\n")
        return

    print(f"\nFound {len(matches)} matching student(s):")
    display_students(matches)


def show_menu():
    print("Student Grade Calculator")
    print("------------------------")
    print("1. Add new student record")
    print("2. Display all students")
    print("3. Search student by name")
    print("4. Show class statistics")
    print("5. Save records to file")
    print("Press ESC to exit")
    print("Choice: ", end="", flush=True)


def main():
    records = load_records(DATA_FILE)
    if records:
        print(f"Loaded {len(records)} record(s) from {DATA_FILE}.\n")
    else:
        print(f"No saved records found. Starting with an empty grade book.\n")

    while True:
        show_menu()
        choice = get_single_keypress()
        if choice == "\x1b":
            print("\nExiting program.")
            save_records(DATA_FILE, records)
            break

        print(choice)
        if choice == "1":
            add_student(records)
        elif choice == "2":
            display_students(records)
        elif choice == "3":
            search_by_name(records)
        elif choice == "4":
            display_statistics(records)
        elif choice == "5":
            save_records(DATA_FILE, records)
        else:
            print("Invalid selection. Please choose a number from 1 to 5, or press ESC to exit.\n")

    print("Goodbye!")


if __name__ == "__main__":
    main()
