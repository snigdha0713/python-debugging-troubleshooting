"""Read student marks from CSV and create a text summary report."""

import argparse
import csv
import sys
from pathlib import Path

StudentRecord = tuple[str, int]


def load_students(file_path: str | Path) -> list[StudentRecord]:
    """Load validated student names and marks from a CSV file.

    The CSV file must contain a header with the columns Name and Marks.
    Blank lines are ignored; invalid records are reported with their row number.
    """
    path = Path(file_path)
    students: list[StudentRecord] = []

    with path.open("r", encoding="utf-8-sig", newline="") as input_file:
        reader = csv.reader(input_file)
        header = next(reader, None)
        if header is None:
            raise ValueError("The input CSV file is empty.")

        normalized_header = [column.strip().lower() for column in header]
        if normalized_header != ["name", "marks"]:
            raise ValueError("The CSV header must contain exactly: Name,Marks.")

        for row_number, row in enumerate(reader, start=2):
            if not row or all(not value.strip() for value in row):
                continue
            if len(row) != 2:
                raise ValueError(
                    f"Row {row_number} must contain a name and one mark value."
                )

            name = row[0].strip()
            mark_text = row[1].strip()
            if not name:
                raise ValueError(f"Row {row_number} has an empty student name.")
            try:
                mark = int(mark_text)
            except ValueError as exc:
                raise ValueError(
                    f"Row {row_number} has a mark that is not a whole number: "
                    f"{mark_text!r}."
                ) from exc

            if not 0 <= mark <= 100:
                raise ValueError(
                    f"Row {row_number} has a mark outside the range 0 to 100."
                )
            students.append((name, mark))

    if not students:
        raise ValueError("The CSV file does not contain any student records.")
    return students


def get_grade(mark: int) -> str:
    """Return the grade for a mark on a 0-100 scale."""
    if type(mark) is not int or not 0 <= mark <= 100:
        raise ValueError("Mark must be a whole number between 0 and 100.")
    if mark >= 90:
        return "A"
    if mark >= 75:
        return "B"
    if mark >= 60:
        return "C"
    if mark >= 40:
        return "D"
    return "F"


def calculate_average(students: list[StudentRecord]) -> float:
    """Return the arithmetic mean of all student marks."""
    if not students:
        raise ValueError("Cannot calculate an average without student records.")
    return sum(mark for _, mark in students) / len(students)


def find_top_student(students: list[StudentRecord]) -> StudentRecord:
    """Return the student with the highest mark.

    When marks are tied, the first student in the input file is returned.
    """
    if not students:
        raise ValueError("Cannot find a top student without student records.")
    return max(students, key=lambda student: student[1])


def build_report(students: list[StudentRecord]) -> str:
    """Build the report text without performing file I/O."""
    average = calculate_average(students)
    top_student = find_top_student(students)
    lines = [
        "STUDENT MARKS REPORT",
        "====================",
        f"Number of students: {len(students)}",
        f"Average mark: {average:.2f}",
        f"Top student: {top_student[0]} ({top_student[1]})",
        "",
        "INDIVIDUAL RESULTS",
    ]
    for name, mark in students:
        lines.append(f"{name}: {mark} - Grade {get_grade(mark)}")
    return "\n".join(lines) + "\n"


def save_report(students: list[StudentRecord], output_path: str | Path) -> None:
    """Write the generated report to the requested text file."""
    report = build_report(students)
    Path(output_path).write_text(report, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run the command-line application and return an exit status."""
    parser = argparse.ArgumentParser(
        description="Create a summary report from a CSV file of student marks."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="sample_data/marks.csv",
        help="CSV input file (default: sample_data/marks.csv)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="report.txt",
        help="text report path (default: report.txt)",
    )
    args = parser.parse_args(argv)

    try:
        students = load_students(args.input)
        save_report(students, args.output)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Report saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
