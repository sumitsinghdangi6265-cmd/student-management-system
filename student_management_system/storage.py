"""Storage implementations for JSON and CSV persistence."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Protocol

from student_management_system.models import Student


class BaseStorage(Protocol):
    """Protocol for storage backends."""

    def load_students(self) -> list[Student]:
        """Load student records from storage."""

    def save_students(self, students: list[Student]) -> None:
        """Persist student records to storage."""


class JSONStorage:
    """Store student data in JSON format."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_students(self) -> list[Student]:
        if not self.file_path.exists():
            return []
        try:
            raw_data = json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        return [Student.from_raw(**item) for item in raw_data]

    def save_students(self, students: list[Student]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [student.to_dict() for student in students]
        self.file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class CSVStorage:
    """Store student data in CSV format."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_students(self) -> list[Student]:
        if not self.file_path.exists():
            return []
        students: list[Student] = []
        with self.file_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                students.append(Student.from_raw(**row))
        return students

    def save_students(self, students: list[Student]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8", newline="") as handle:
            fieldnames = ["student_id", "name", "age", "grade", "marks"]
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student.to_dict())
