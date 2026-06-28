from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    """Represents a course in the university scheduling system.

    Attributes:
        course_id: Unique identifier for the course (e.g., 'KOM120').
        course_name: Full name of the course (e.g., 'Struktur Data').
        faculty_id: Faculty offering the course (e.g., 'FMIPA' or 'GENERAL').
        department_id: Department offering the course (e.g., 'ILKOM' or 'GENERAL').
        offered_semester: The semester in which the course is offered (1 to 8).
        course_type: The type of course (e.g., 'GENERAL', 'FACULTY',
            'DEPARTMENT', 'ELECTIVE').
    """

    course_id: str
    course_name: str
    faculty_id: str
    department_id: str
    offered_semester: int
    course_type: str
    room_id: str = ""
