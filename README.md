# Python Debugging and Troubleshooting

A Python project for reviewing an existing script, reproducing its problems, correcting the underlying causes, and recording the debugging process.

## Project status

The repository is set up for the Week 2 task. The original Python script has not yet been provided, so the bug report, corrected script, and final debugging log will be completed after the original file is available. No bugs or test results are being assumed in advance.

## Planned folder structure

```text
python-debugging-troubleshooting/
├── original_script/
│   └── (original script supplied for the task)
├── corrected_script/
│   └── (corrected version after debugging)
├── documentation/
│   └── DEBUGGING_LOG.md
├── tests/
│   └── (tests based on the actual script)
├── README.md
├── requirements.txt
└── .gitignore
```

The folder and file names may be adjusted if the supplied script needs related files, sample input, or other dependencies.

## Work plan

1. Review the supplied script and understand its intended behaviour.
2. Run it with normal and edge-case inputs to establish a baseline.
3. Record each reproducible issue, including the input, observed behaviour, expected behaviour, and relevant error message.
4. Trace the issue to its cause using appropriate tools. Python's built-in debugger (`pdb`) may be used where line-by-line inspection is useful.
5. Make focused corrections and explain why each change is needed.
6. Add tests that cover the original failures and normal use cases.
7. Run the tests and record the actual results.
8. Review the final code for readability and maintainability without changing its intended behaviour.

## Running the project

Run instructions and dependencies will be added after the original script is reviewed. The final steps will depend on the supplied program and its required packages.

## Final deliverables

- Original script retained for comparison.
- Corrected Python script.
- A debugging log explaining the reproduced issues, root causes, fixes, and verification.
- Tests or clear manual test instructions.
- A self-contained ZIP archive containing the final files.
