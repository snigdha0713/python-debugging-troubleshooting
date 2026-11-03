# Week 2 - Python Debugging and Troubleshooting

## Project: Student Marks Report

This project demonstrates a debugging exercise using a small Python program that reads student marks from a CSV file and creates a text report.

### Why this project uses a self-created starter script

No starter Python script was supplied with the internship task. To complete the exercise without claiming that an external script was provided, a sample program was created for this project. The file in original_script contains deliberate, reproducible defects. The corrected version is in corrected_script, and the investigation is recorded in documentation/DEBUGGING_LOG.md.

The original script is kept unchanged so that its behaviour can be compared with the corrected program.

## Project structure

    python-debugging-troubleshooting/
    ├── original_script/
    │   ├── __init__.py
    │   └── grade_report.py
    ├── corrected_script/
    │   ├── __init__.py
    │   └── grade_report.py
    ├── documentation/
    │   └── DEBUGGING_LOG.md
    ├── tests/
    │   ├── __init__.py
    │   └── test_grade_report.py
    ├── sample_data/
    │   ├── marks.csv
    │   └── expected_report.txt
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## What the program does

The corrected program reads a CSV file with two columns, Name and Marks. It validates the records, calculates the average, identifies the student with the highest mark, assigns a grade to each student, and writes a text report.

For this exercise, the grade bands are A = 90-100, B = 75-89, C = 60-74, D = 40-59, and F = 0-39. These bands are project assumptions used to make the example testable; they were not supplied as part of the internship instructions.

## Requirements

- Python 3.10 or newer
- No third-party packages are required

Check the installed version with:

    python --version

## Run the corrected application

From the root folder of the project, run:

    python corrected_script/grade_report.py sample_data/marks.csv report.txt

The program prints a confirmation and writes report.txt in the current folder. Input and output paths can be changed:

    python corrected_script/grade_report.py path/to/marks.csv path/to/report.txt

The input CSV must have this header and data format:

    Name,Marks
    Asha,85
    Ravi,72
    Mina,98

The corrected program reports missing files, invalid headers, malformed rows, non-numeric marks, marks outside 0-100, and files with no student records. It does not silently ignore invalid student records.

## Run the tests

From the root folder:

    python -m unittest discover -s tests -v

The tests use temporary files and do not modify sample_data/marks.csv.

## Debugging log

The detailed bug report, reproduction steps, error messages, root causes, before-and-after code examples, use of pdb, fixes, and test results are in documentation/DEBUGGING_LOG.md.

## Deliverables

- original_script/grade_report.py: the deliberately faulty starter program created for this exercise.
- corrected_script/grade_report.py: the corrected program.
- documentation/DEBUGGING_LOG.md: the debugging record.
- tests/: automated regression and validation tests.
- sample_data/marks.csv: sample input file.
- sample_data/expected_report.txt: expected output for the sample data.

The original script is included for comparison and should not be used as the final application. Run the corrected script for normal use.
