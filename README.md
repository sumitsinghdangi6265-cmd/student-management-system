# Student Management System

## Overview

This project is a modular Python-based Student Management System built for academic demonstration purposes. It allows an administrator to manage student records with persistent storage in both JSON and CSV formats.

## Features

- Admin login authentication
- Add, update, delete, and search student records
- Store data using JSON and CSV files
- Sort records by name or marks
- Generate reports such as topper and average marks
- Validate input and handle invalid entries gracefully
- Maintain a modular, well-structured codebase

## Project Structure

```text
student_management_system/
|-- config/
|   `-- admin_credentials.txt
|-- data/
|   |-- students.csv
|   `-- students.json
|-- student_management_system/
|   |-- __init__.py
|   |-- auth.py
|   |-- cli.py
|   |-- models.py
|   |-- service.py
|   `-- storage.py
|-- main.py
`-- README.md
```

## Technologies Used

- Python 3
- JSON for primary persistence
- CSV for backup/export-style storage

## Default Admin Credentials

- Username: `admin`
- Password: `admin123`

You can change these values in `config/admin_credentials.txt`. The password is stored as a SHA-256 hash.

## How to Run

1. Open a terminal in the project directory:

   ```powershell
   cd student_management_system
   ```

2. Run the application:

   ```powershell
   python main.py
   ```

## Main Functionalities

### Add Student

Create a new student record with ID, name, age, grade, and marks.

### Update Student

Modify an existing student record while preserving fields you do not want to change.

### Delete Student

Remove a student record permanently using the student ID.

### Search Student

Find a student by exact ID or by partial name match.

### Sort Students

Display records sorted alphabetically by name or numerically by marks.

### Reports

Generate a quick summary including:

- Total number of students
- Average marks
- Top-performing student

## Exception Handling

The program validates:

- Empty student IDs, names, or grades
- Non-numeric ages
- Marks outside the `0` to `100` range
- Duplicate student IDs

## Demonstration Checklist

Use this sequence during your project demo:

1. Log in with the admin credentials.
2. View the seeded student records.
3. Add a new student.
4. Search for the new student by name.
5. Update the student marks.
6. Sort students by marks.
7. Generate the report summary.
8. Delete the added student.
9. Re-open `data/students.json` or `data/students.csv` to show persisted changes.

## GitHub Submission

To upload this project to GitHub, initialize a Git repository, create a remote repository, commit the files, and push the project once Git is available on your machine.
