"""Automated tests for the corrected student marks report program."""

import tempfile
import unittest
from pathlib import Path

from corrected_script.grade_report import (
    build_report,
    calculate_average,
    find_top_student,
    get_grade,
    load_students,
    save_report,
)


class GradeCalculationTests(unittest.TestCase):
    def test_grade_boundaries(self):
        expected = {100: "A", 90: "A", 89: "B", 75: "B", 74: "C",
                    60: "C", 59: "D", 40: "D", 39: "F", 0: "F"}
        for mark, grade in expected.items():
            with self.subTest(mark=mark):
                self.assertEqual(get_grade(mark), grade)

    def test_grade_rejects_out_of_range_marks(self):
        for mark in (-1, 101):
            with self.subTest(mark=mark):
                with self.assertRaises(ValueError):
                    get_grade(mark)

    def test_grade_rejects_non_integer_marks(self):
        with self.assertRaises(ValueError):
            get_grade(75.5)

    def test_average_uses_all_students(self):
        self.assertEqual(calculate_average([("Asha", 85), ("Ravi", 72), ("Mina", 98)]), 85)

    def test_average_with_one_student(self):
        self.assertEqual(calculate_average([("Asha", 84)]), 84)

    def test_average_rejects_empty_list(self):
        with self.assertRaises(ValueError):
            calculate_average([])

    def test_top_student_can_be_last_record(self):
        students = [("Asha", 85), ("Ravi", 72), ("Mina", 98)]
        self.assertEqual(find_top_student(students), ("Mina", 98))

    def test_top_student_keeps_first_student_when_marks_tie(self):
        students = [("Asha", 95), ("Ravi", 95)]
        self.assertEqual(find_top_student(students), ("Asha", 95))

    def test_top_student_rejects_empty_list(self):
        with self.assertRaises(ValueError):
            find_top_student([])


class CsvAndReportTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_csv(self, text):
        path = self.folder / "marks.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_loads_header_and_student_rows(self):
        path = self.write_csv("Name,Marks\nAsha,85\nRavi,72\n")
        self.assertEqual(load_students(path), [("Asha", 85), ("Ravi", 72)])

    def test_load_ignores_blank_lines(self):
        path = self.write_csv("Name,Marks\nAsha,85\n\nRavi,72\n")
        self.assertEqual(load_students(path), [("Asha", 85), ("Ravi", 72)])

    def test_rejects_wrong_header(self):
        path = self.write_csv("Student,Score\nAsha,85\n")
        with self.assertRaisesRegex(ValueError, "header"):
            load_students(path)

    def test_rejects_non_numeric_mark(self):
        path = self.write_csv("Name,Marks\nAsha,eighty\n")
        with self.assertRaisesRegex(ValueError, "whole number"):
            load_students(path)

    def test_rejects_out_of_range_mark(self):
        path = self.write_csv("Name,Marks\nAsha,105\n")
        with self.assertRaisesRegex(ValueError, "range 0 to 100"):
            load_students(path)

    def test_rejects_malformed_row(self):
        path = self.write_csv("Name,Marks\nAsha,85,extra\n")
        with self.assertRaisesRegex(ValueError, "Row 2"):
            load_students(path)

    def test_rejects_file_with_header_only(self):
        path = self.write_csv("Name,Marks\n")
        with self.assertRaisesRegex(ValueError, "does not contain"):
            load_students(path)

    def test_missing_input_file_raises_clear_file_error(self):
        with self.assertRaises(FileNotFoundError):
            load_students(self.folder / "missing.csv")

    def test_report_contains_summary_and_individual_results(self):
        report = build_report([("Asha", 85), ("Ravi", 72), ("Mina", 98)])
        self.assertIn("Number of students: 3", report)
        self.assertIn("Average mark: 85.00", report)
        self.assertIn("Top student: Mina (98)", report)
        self.assertIn("Mina: 98 - Grade A", report)

    def test_save_report_writes_file(self):
        output = self.folder / "report.txt"
        save_report([("Asha", 85)], output)
        self.assertIn("Asha: 85 - Grade B", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
