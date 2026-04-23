"""Command-line interface for the Student Management System."""

from __future__ import annotations

from getpass import getpass
from pathlib import Path

from student_management_system.auth import Authenticator
from student_management_system.models import Student
from student_management_system.service import StudentService
from student_management_system.storage import CSVStorage, JSONStorage


class StudentManagementCLI:
    """Interactive CLI used by administrators."""

    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        data_dir = base_dir / "data"
        credentials_file = base_dir / "config" / "admin_credentials.txt"

        self.authenticator = Authenticator(credentials_file)
        self.service = StudentService(
            primary_storage=JSONStorage(data_dir / "students.json"),
            backup_storage=CSVStorage(data_dir / "students.csv"),
        )
        self.menu_actions = {
            "1": self.add_student,
            "2": self.update_student,
            "3": self.delete_student,
            "4": self.search_students,
            "5": self.view_all_students,
            "6": self.sort_students,
            "7": self.generate_reports,
            "8": self.exit_program,
        }
        self.is_running = True

    def run(self) -> None:
        """Start the application lifecycle."""
        self._display_header()
        if not self._login():
            print("Too many failed login attempts. Exiting application.")
            return

        while self.is_running:
            self._show_menu()
            choice = input("Enter your choice: ").strip()
            action = self.menu_actions.get(choice)
            if action is None:
                print("Invalid menu choice. Please select a valid option.")
                continue
            action()

    def _display_header(self) -> None:
        print("=" * 55)
        print("        Student Management System")
        print("=" * 55)

    def _login(self) -> bool:
        """Prompt for admin credentials with a fixed attempt count."""
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            print(f"\nAdmin Login ({attempt}/{max_attempts})")
            username = input("Username: ").strip()
            password = getpass("Password: ")
            if self.authenticator.authenticate(username, password):
                print("\nLogin successful.\n")
                return True
            print("Invalid username or password.")
        return False

    def _show_menu(self) -> None:
        print("\nMenu")
        print("1. Add student")
        print("2. Update student")
        print("3. Delete student")
        print("4. Search student")
        print("5. View all students")
        print("6. Sort students")
        print("7. Generate reports")
        print("8. Exit")

    def add_student(self) -> None:
        """Collect and save a new student record."""
        try:
            student = self._collect_student_data()
            self.service.add_student(student)
            print("Student added successfully.")
        except ValueError as error:
            print(f"Error: {error}")

    def update_student(self) -> None:
        """Update a student record based on student ID."""
        student_id = input("Enter student ID to update: ").strip()
        try:
            existing = self.service.get_student_by_id(student_id)
            if existing is None:
                print("Student not found.")
                return

            print("Leave a field blank to keep the current value.")
            updated_student = self._collect_student_data(existing)
            self.service.update_student(student_id, updated_student)
            print("Student updated successfully.")
        except ValueError as error:
            print(f"Error: {error}")

    def delete_student(self) -> None:
        """Delete a student by ID."""
        student_id = input("Enter student ID to delete: ").strip()
        if self.service.delete_student(student_id):
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def search_students(self) -> None:
        """Search students by ID or partial name."""
        query = input("Enter student ID or name to search: ").strip()
        matches = self.service.search_students(query)
        if not matches:
            print("No matching students found.")
            return
        self._print_students(matches)

    def view_all_students(self) -> None:
        """Display all stored student records."""
        students = self.service.get_all_students()
        if not students:
            print("No student records available.")
            return
        self._print_students(students)

    def sort_students(self) -> None:
        """Sort students by name or marks."""
        key = input("Sort by 'name' or 'marks': ").strip().lower()
        if key not in {"name", "marks"}:
            print("Invalid sort option.")
            return

        descending = input("Descending order? (y/n): ").strip().lower() == "y"
        students = self.service.sort_students(key=key, descending=descending)
        self._print_students(students)

    def generate_reports(self) -> None:
        """Display summary reports for the current dataset."""
        report = self.service.generate_report()
        print("\nReport Summary")
        print(f"Total students: {report['total_students']}")
        print(f"Average marks: {report['average_marks']:.2f}")
        topper = report["topper"]
        if topper is None:
            print("Topper: Not available")
        else:
            print(
                "Topper: "
                f"{topper.name} ({topper.student_id}) with {topper.marks:.2f} marks"
            )

    def exit_program(self) -> None:
        """Exit the CLI loop."""
        self.is_running = False
        print("Exiting Student Management System.")

    def _collect_student_data(self, existing: Student | None = None) -> Student:
        """Prompt for student fields and validate the result."""
        student_id = self._read_value("Student ID", existing.student_id if existing else "")
        name = self._read_value("Name", existing.name if existing else "")
        age_text = self._read_value("Age", str(existing.age) if existing else "")
        grade = self._read_value("Grade", existing.grade if existing else "")
        marks_text = self._read_value("Marks", str(existing.marks) if existing else "")

        return Student.from_raw(
            student_id=student_id,
            name=name,
            age=age_text,
            grade=grade,
            marks=marks_text,
        )

    @staticmethod
    def _read_value(label: str, current_value: str) -> str:
        prompt = f"{label}"
        if current_value:
            prompt += f" [{current_value}]"
        prompt += ": "
        value = input(prompt).strip()
        return value if value else current_value

    @staticmethod
    def _print_students(students: list[Student]) -> None:
        """Print student data in a table-like format."""
        print("\n{:<12} {:<20} {:<8} {:<10} {:<10}".format(
            "Student ID", "Name", "Age", "Grade", "Marks"
        ))
        print("-" * 64)
        for student in students:
            print(
                "{:<12} {:<20} {:<8} {:<10} {:<10.2f}".format(
                    student.student_id,
                    student.name,
                    student.age,
                    student.grade,
                    student.marks,
                )
            )
