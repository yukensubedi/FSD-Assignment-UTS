
# CLIUniApp & GUIUniApp (Python)

This project implements the UTS Assessment 1 – Part 2 & 3 specification in Python:
- **CLI** application for University System, Student System, Subject Enrolment System, and Admin System.
- **GUI** (challenge) with login + enrolment + subject list + simple exceptions using Tkinter.

## Features
- File persistence using `students.data` (pickle-serialized Student objects).
- Student Registration & Login with regex validation:
  - Email must end with `@university.com`
  - Password must start with uppercase, have at least 5 letters total, and end with 3+ digits.
- Subject enrolment (max 4), removal, password change, show subjects with marks/grades/average.
- Admin operations: show all, group by overall grade, partition pass/fail, remove by ID, clear database.

## Run (CLI)
```bash
python -m cliuniapp.main
```

## Run (GUI)
```bash
python -m cliuniapp.gui.gui_uni_app
```

> Ensure your working directory is the parent of the `cliuniapp/` folder so Python can import the package.

## Notes
- Grade bands used: `HD >=85`, `D >=75`, `C >=65`, `P >=50`, else `F`.
- All changes are persisted to `students.data` in the current working directory.
- The GUI reads/writes the same `students.data` file.

## Folder Structure
```
cliuniapp/
  controllers/
    admin_controller.py
    student_controller.py
    university_system.py
  gui/
    gui_uni_app.py
  models/
    database.py
    student.py
    subject.py
  main.py
  students.data (created on first run)
```

## Python Version
Tested on Python 3.10+
