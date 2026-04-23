"""Data models used by the Student Management System."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Student:
    """Represents a single student record."""

    student_id: str
    name: str
    age: int
    grade: str
    marks: float

    @classmethod
    def from_raw(
        cls,
        student_id: str,
        name: str,
        age: str | int,
        grade: str,
        marks: str | float,
    ) -> "Student":
        """Validate raw input and create a Student instance."""
        student_id = str(student_id).strip()
        name = str(name).strip()
        grade = str(grade).strip()

        if not student_id:
            raise ValueError("Student ID cannot be empty.")
        if not name:
            raise ValueError("Student name cannot be empty.")
        if not grade:
            raise ValueError("Grade cannot be empty.")

        try:
            validated_age = int(age)
        except (TypeError, ValueError) as error:
            raise ValueError("Age must be a whole number.") from error
        if validated_age <= 0:
            raise ValueError("Age must be greater than zero.")

        try:
            validated_marks = float(marks)
        except (TypeError, ValueError) as error:
            raise ValueError("Marks must be a numeric value.") from error
        if not 0 <= validated_marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        return cls(
            student_id=student_id,
            name=name,
            age=validated_age,
            grade=grade,
            marks=validated_marks,
        )

    def to_dict(self) -> dict[str, str | int | float]:
        """Convert the dataclass to a serializable dictionary."""
        return asdict(self)
