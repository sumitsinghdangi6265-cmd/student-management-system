"""Business logic for managing student records."""

from __future__ import annotations

from student_management_system.models import Student
from student_management_system.storage import BaseStorage


class StudentService:
    """Coordinates student operations and persistent storage."""

    def __init__(self, primary_storage: BaseStorage, backup_storage: BaseStorage) -> None:
        self.primary_storage = primary_storage
        self.backup_storage = backup_storage
        self._bootstrap_if_needed()

    def _bootstrap_if_needed(self) -> None:
        """Ensure a starter dataset exists for both storage formats."""
        students = self.primary_storage.load_students()
        if students:
            self.backup_storage.save_students(students)
            return

        students = self.backup_storage.load_students()
        if students:
            self.primary_storage.save_students(students)
            return

        seed_students = [
            Student(student_id="S101", name="Aarav Sharma", age=16, grade="10", marks=91.5),
            Student(student_id="S102", name="Diya Verma", age=15, grade="9", marks=88.0),
            Student(student_id="S103", name="Kabir Singh", age=17, grade="11", marks=95.0),
        ]
        self._save(seed_students)

    def _load(self) -> list[Student]:
        return self.primary_storage.load_students()

    def _save(self, students: list[Student]) -> None:
        self.primary_storage.save_students(students)
        self.backup_storage.save_students(students)

    def get_all_students(self) -> list[Student]:
        """Return all students."""
        return self._load()

    def get_student_by_id(self, student_id: str) -> Student | None:
        """Return a student by ID, if present."""
        for student in self._load():
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def add_student(self, student: Student) -> None:
        """Add a new student if the ID is unique."""
        students = self._load()
        if any(item.student_id.lower() == student.student_id.lower() for item in students):
            raise ValueError("A student with this ID already exists.")
        students.append(student)
        self._save(students)

    def update_student(self, student_id: str, updated_student: Student) -> bool:
        """Replace the stored record for the given student ID."""
        students = self._load()
        for index, student in enumerate(students):
            if student.student_id.lower() != student_id.lower():
                continue

            for other in students:
                if (
                    other.student_id.lower() == updated_student.student_id.lower()
                    and other.student_id.lower() != student_id.lower()
                ):
                    raise ValueError("Another student already uses the requested ID.")

            students[index] = updated_student
            self._save(students)
            return True
        return False

    def delete_student(self, student_id: str) -> bool:
        """Delete a student by ID."""
        students = self._load()
        remaining = [
            student for student in students if student.student_id.lower() != student_id.lower()
        ]
        if len(remaining) == len(students):
            return False
        self._save(remaining)
        return True

    def search_students(self, query: str) -> list[Student]:
        """Search by exact student ID or partial name match."""
        query = query.strip().lower()
        if not query:
            return []
        return [
            student
            for student in self._load()
            if query == student.student_id.lower() or query in student.name.lower()
        ]

    def sort_students(self, key: str, descending: bool = False) -> list[Student]:
        """Return students sorted by name or marks."""
        students = self._load()
        if key == "name":
            return sorted(students, key=lambda student: student.name.lower(), reverse=descending)
        if key == "marks":
            return sorted(students, key=lambda student: student.marks, reverse=descending)
        raise ValueError("Unsupported sort key.")

    def generate_report(self) -> dict[str, int | float | Student | None]:
        """Generate summary metrics for the current student dataset."""
        students = self._load()
        if not students:
            return {"total_students": 0, "average_marks": 0.0, "topper": None}

        total_students = len(students)
        average_marks = sum(student.marks for student in students) / total_students
        topper = max(students, key=lambda student: student.marks)
        return {
            "total_students": total_students,
            "average_marks": average_marks,
            "topper": topper,
        }
