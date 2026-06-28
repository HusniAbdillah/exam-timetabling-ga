from dataclasses import dataclass


@dataclass(frozen=True)
class Enrollment:
    """Represents a student's enrollment in a course.

    Attributes:
        student_id: ID of the enrolled student.
        course_id: ID of the course the student is taking.
    """

    student_id: str
    course_id: str
