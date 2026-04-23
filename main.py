"""Application entry point for the Student Management System."""

from student_management_system.cli import StudentManagementCLI


def main() -> None:
    """Start the command-line interface."""
    app = StudentManagementCLI()
    app.run()


if __name__ == "__main__":
    main()
