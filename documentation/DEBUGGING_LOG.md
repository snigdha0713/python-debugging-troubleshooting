# Debugging Log - Student Marks Report

## Project details

**Task:** Week 2 - Debugging and Troubleshooting Python Applications  
**Program:** Student Marks Report  
**Language:** Python  
**External starter script:** Not supplied with the internship task  
**Approach:** A small starter program was written for this exercise with deliberate defects. The defects below were reproduced, investigated, corrected, and tested. The original version is retained in original_script/grade_report.py for comparison.

## 1. Intended behaviour

The program should read a CSV file containing student names and marks, calculate the class average, identify the student with the highest mark, assign a grade to each student, and save a readable text report.

The expected CSV structure is:

    Name,Marks
    Asha,85
    Ravi,72
    Mina,98

For this exercise, the grading boundaries are A = 90-100, B = 75-89, C = 60-74, D = 40-59, and F = 0-39. These boundaries were selected for the sample program because the task description did not give a grading scale.

With the sample data, the expected average is 85.00 and the top student is Mina with 98 marks.

## 2. Initial code review

The first review focused on the parts of the program most likely to cause trouble:

- File opening and closing in load_students.
- Splitting input lines and converting marks to integers.
- The loop used to calculate the average.
- The loop used to find the top student.
- The comparison operators used to assign grades.
- The creation of the output report.

The original program used a manually opened file, did not distinguish a CSV header from a data row, did not validate the number or type of fields, and did not check whether the list of students was empty before calculating results.

## 3. Bug report and investigation

### BUG-01 - The CSV header is treated as a student record

**Location:** original_script/grade_report.py, load_students, lines 18-20.

**Reproduction:**

    python original_script/grade_report.py sample_data/marks.csv /tmp/report.txt

**Observed error:**

    ValueError: invalid literal for int() with base 10: 'Marks'

**Expected behaviour:** The first row should be recognised as the column header and should not be converted into a student mark.

**Root cause:** The original loop processes every line as a data row. It splits Name,Marks and then attempts to convert the word Marks to an integer.

**Original code:**

    for line in file:
        name, mark = line.strip().split(",")
        students.append((name, int(mark)))

**Correction:** The revised loader uses csv.reader, reads and checks the header once, and starts processing student records from the following row.

    reader = csv.reader(input_file)
    header = next(reader, None)
    if header is None:
        raise ValueError("The input CSV file is empty.")

    normalized_header = [column.strip().lower() for column in header]
    if normalized_header != ["name", "marks"]:
        raise ValueError("The CSV header must contain exactly: Name,Marks.")

**Verification:** The corrected loader reads the sample file and returns three student records. This is covered by test_loads_header_and_student_rows.

### BUG-02 - Missing input file causes an unbound local variable error

**Location:** original_script/grade_report.py, load_students, lines 13-18.

**Reproduction:**

    python original_script/grade_report.py sample_data/not_found.csv /tmp/report.txt

**Observed output:**

    The input file was not found.
    UnboundLocalError: cannot access local variable 'file' where it is not associated with a value

**Expected behaviour:** The program should stop the operation with a clear file error. It should not continue to the file-reading loop.

**Root cause:** The exception handler prints a message but does not return or raise an error. Since open() failed, the variable file was never assigned, but the next loop still tries to use it.

**Original code:**

    try:
        file = open(file_path, "r")
    except FileNotFoundError:
        print("The input file was not found.")

    for line in file:
        ...

**Correction:** The revised loader uses a with statement. A missing-file exception is allowed to reach main, where it is caught and displayed as a concise error. The program returns a non-zero exit status.

    with path.open("r", encoding="utf-8-sig", newline="") as input_file:
        reader = csv.reader(input_file)

**Verification:** test_missing_input_file_raises_clear_file_error confirms that the loader raises FileNotFoundError rather than attempting to read an undefined variable. The command-line entry point handles the exception.

### BUG-03 - Average calculation uses the wrong denominator

**Location:** original_script/grade_report.py, calculate_average, line 37.

**Reproduction:**

    from original_script.grade_report import calculate_average

    students = [("Asha", 85), ("Ravi", 72), ("Mina", 98)]
    print(calculate_average(students))

**Observed result:** 127.5  
**Expected result:** 85.0

The total is 255. The average of three marks is 255 divided by 3, not 255 divided by 2. With a single student, the original formula also raises ZeroDivisionError: division by zero.

**Root cause:** The expression uses len(students) - 1, even though the number of values being added is the full length of the list.

**Original code:**

    return total / (len(students) - 1)

**Correction:** The revised function checks for an empty list and divides the sum by the actual number of student records.

    if not students:
        raise ValueError("Cannot calculate an average without student records.")
    return sum(mark for _, mark in students) / len(students)

**Verification:** Tests confirm the average for three students, the result for a single student, and the error raised for an empty list.

### BUG-04 - The last student is skipped when finding the top mark

**Location:** original_script/grade_report.py, find_top_student, line 45.

**Reproduction:**

    from original_script.grade_report import find_top_student

    students = [("Asha", 85), ("Ravi", 72), ("Mina", 98)]
    print(find_top_student(students))

**Observed result:** ('Asha', 85)  
**Expected result:** ('Mina', 98)

**Root cause:** range(len(students) - 1) stops before the last list index. The final student is never checked.

**Original code:**

    for index in range(len(students) - 1):
        if students[index][1] > top_student[1]:
            top_student = students[index]

**Correction:** The revised function uses max with the mark as its key. It also checks for an empty list before searching.

    if not students:
        raise ValueError("Cannot find a top student without student records.")
    return max(students, key=lambda student: student[1])

**Verification:** test_top_student_can_be_last_record confirms that the final student is considered. A separate test checks that the first student is retained when the highest mark is tied.

### BUG-05 - Grade boundaries are too strict

**Location:** original_script/grade_report.py, get_grade, lines 25-34.

**Reproduction:**

    from original_script.grade_report import get_grade

    for mark in (90, 75, 60, 40):
        print(mark, get_grade(mark))

**Observed boundary results:** 90 gives B, 75 gives C, 60 gives D, and 40 gives F.  
**Expected boundary results for this exercise:** 90 gives A, 75 gives B, 60 gives C, and 40 gives D.

**Root cause:** The original conditions use > instead of >=. A mark equal to a boundary therefore falls into the lower grade band.

**Original code:**

    if mark > 90:
        return "A"
    elif mark > 75:
        return "B"

**Correction:** The revised function validates the mark range and uses inclusive lower limits for each grade band.

    if mark >= 90:
        return "A"
    if mark >= 75:
        return "B"

**Verification:** test_grade_boundaries checks values on both sides of each boundary, including 90, 75, 60, and 40. The chosen grading bands are documented in the README.

### BUG-06 - Input rows and marks are not validated

**Location:** original_script/grade_report.py, load_students, line 19.

**Reproduction:** A row with an extra CSV field, such as Asha,85,extra, causes:

    ValueError: too many values to unpack (expected 2)

A non-numeric mark also fails during integer conversion. Blank names and marks outside the normal 0-100 range are not checked before they are added to the list.

**Expected behaviour:** The loader should report which row is invalid and explain whether the problem is the number of columns, the name, the mark format, or the mark range.

**Root cause:** The original program assumes every line always contains exactly two valid comma-separated values and that the second value is a valid mark.

**Original code:**

    name, mark = line.strip().split(",")
    students.append((name, int(mark)))

**Correction:** The revised loader checks the number of columns, requires a non-empty name, converts the mark with a specific error message, and checks that the mark is between 0 and 100. It also ignores completely blank lines and rejects a file with no student records.

**Verification:** Tests cover an incorrect header, an extra CSV field, non-numeric marks, out-of-range marks, blank lines, and a header-only file.

## 4. Debugger use

Python's built-in pdb debugger was used to step through load_students while loading the sample CSV. The function was invoked under the debugger using this command (the piped commands automate the interactive steps):

    printf 'next\nnext\nnext\nnext\np line\nnext\nwhere\nquit\n' | python -c "import pdb; from original_script.grade_report import load_students; pdb.runcall(load_students, 'sample_data/marks.csv')"

The debugger was stepped through the file-opening and line-reading statements. At the parsing statement, p line displayed Name,Marks followed by a newline. This showed that the header was being treated as a data row. The next statement attempted to convert the word Marks into an integer. The failure was also reproduced in a normal run to capture the full traceback.

Useful debugger commands for repeating the inspection are next to move to the next line, p line to display the current CSV line, and where to show the call stack.

## 5. Code structure and quality improvements

The corrected version includes the following improvements in addition to the specific bug fixes:

- Uses with for file handling so files are closed reliably.
- Uses Python's csv module rather than manually splitting lines.
- Separates loading, validation, calculations, report generation, and saving into individual functions.
- Uses descriptive function and variable names, type hints, and docstrings.
- Checks empty input before calculating an average or finding the top student.
- Uses argparse for input and output paths.
- Displays user-friendly errors and returns a non-zero exit status when the report cannot be created.
- Builds the report text separately from writing it, which makes the report easier to test.

The original program's intended result is preserved: read student marks and create a report with an average, a top student, and each student's grade.

## 6. Testing and verification

The corrected program was tested with Python's built-in unittest framework.

Command used:

    python -m unittest discover -s tests -v

**Result:** 19 tests passed, 0 failures, 0 errors.

The test coverage includes:

- Grade boundaries and invalid marks.
- Average calculations with multiple students, one student, and no students.
- Top-student selection when the highest mark is last and when marks are tied.
- CSV header handling and blank lines.
- Wrong headers, malformed rows, non-numeric marks, and marks outside 0-100.
- Missing and empty input files.
- Report content and report-file writing.

The corrected sample command was also run:

    python corrected_script/grade_report.py sample_data/marks.csv /tmp/week2_corrected_report.txt

It completed successfully. The report showed 3 students, an average mark of 85.00, and Mina as the top student with 98 marks. Individual grades were Asha: B, Ravi: C, and Mina: A.

## 7. Conclusion

The debugging exercise identified and corrected six problem areas involving file handling, CSV parsing, arithmetic, loop boundaries, conditional boundaries, and input validation. The corrected program was checked with automated tests and a sample command-line run. The original file remains in the repository so the faulty and corrected versions can be compared.

The starter program in this project was created specifically for this exercise because no original script was supplied with the internship task.
