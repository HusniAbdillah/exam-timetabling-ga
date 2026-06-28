from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    """Represents a student in the university scheduling system.

    Attributes:
        student_id: Unique identifier for the student (e.g., 'S0001').
        faculty_id: The faculty the student belongs to (e.g., 'FMIPA').
        department_id: The department/major of the student (e.g., 'ILKOM').
        current_semester: The active semester of the student (1 to 8).
    """

    student_id: str
    faculty_id: str
    department_id: str
    current_semester: int
