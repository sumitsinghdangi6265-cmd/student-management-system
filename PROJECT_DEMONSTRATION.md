# Project Demonstration Script

## Introduction

This Student Management System is a command-line project designed to manage academic records efficiently. It uses modular Python code, file-based persistence, and input validation to provide a reliable admin-controlled workflow.

## Demo Flow

1. Start the application using `python main.py`.
2. Log in with the admin account.
3. Show the menu and explain each option briefly.
4. Open the "View all students" option to display the current dataset.
5. Add a new student record and mention input validation rules.
6. Search the student by ID and by name.
7. Update the same student and explain how unchanged values can be retained.
8. Sort students by marks to show ranking behavior.
9. Generate reports to show the topper and average marks.
10. Delete the sample student record.
11. Open the CSV or JSON file to demonstrate persistent storage.

## Key Talking Points

- The project is modular, making the code easier to maintain and extend.
- Authentication restricts access to administrative actions.
- Student data is saved in both JSON and CSV formats.
- Exception handling protects the system from invalid inputs.
- Reports provide useful academic insights from stored records.

## Suggested Viva Questions

### Why use both JSON and CSV?

JSON is convenient for structured storage, while CSV is useful for interoperability and easy viewing.

### How is modularity achieved?

The code is split into authentication, storage, business logic, models, and CLI layers.

### How are invalid inputs handled?

The `Student.from_raw()` validator raises descriptive exceptions, which the CLI catches and presents clearly.
