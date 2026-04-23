# GitHub Upload Guide

## Recommended Repository Name

`student-management-system`

## Suggested Commands

Run these commands after installing Git and creating an empty GitHub repository:

```powershell
cd student_management_system
git init
git branch -M main
git add .
git commit -m "Add Student Management System project"
git remote add origin https://github.com/<your-username>/student-management-system.git
git push -u origin main
```

## Before Uploading

- Confirm the README is updated with your name, class, or assignment details if required.
- Run the project once locally to verify the login and menu flow.
- Ensure both `students.json` and `students.csv` are present.

## What to Mention in Submission

- The project uses modular Python code.
- Data is persisted in JSON and CSV files.
- Authentication, reporting, sorting, and exception handling are implemented.
- Documentation and a project demonstration script are included in the repository.
