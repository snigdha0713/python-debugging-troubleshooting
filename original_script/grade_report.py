"""Starter program for the student marks report debugging exercise.

This file intentionally contains defects for the Week 2 debugging exercise.
It is not the corrected application.
"""

import sys


def load_students(file_path):
    students = []
    try:
        file = open(file_path, "r")
    except FileNotFoundError:
        print("The input file was not found.")

    # The original version does not skip the CSV header or validate each row.
    for line in file:
        name, mark = line.strip().split(",")
        students.append((name, int(mark)))

    file.close()
    return students


def get_grade(mark):
    if mark > 90:
        return "A"
    elif mark > 75:
        return "B"
    elif mark > 60:
        return "C"
    elif mark > 40:
        return "D"
    else:
        return "F"


def calculate_average(students):
    total = 0
    for student in students:
        total += student[1]

    # The denominator is one less than the number of students.
    return total / (len(students) - 1)


def find_top_student(students):
    top_student = students[0]

    # The final student is not included in this loop.
    for index in range(len(students) - 1):
        if students[index][1] > top_student[1]:
            top_student = students[index]

    return top_student


def save_report(students, output_path):
    average = calculate_average(students)
    top_student = find_top_student(students)

    with open(output_path, "w") as output_file:
        output_file.write("STUDENT MARKS REPORT\n")
        output_file.write(f"Average: {average:.2f}\n")
        output_file.write(
            f"Top student: {top_student[0]} ({top_student[1]})\n"
        )
        for name, mark in students:
            output_file.write(f"{name}: {mark} - {get_grade(mark)}\n")


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "sample_data/marks.csv"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "report.txt"

    students = load_students(input_path)
    save_report(students, output_path)
    print(f"Report saved to {output_path}")


if __name__ == "__main__":
    main()
