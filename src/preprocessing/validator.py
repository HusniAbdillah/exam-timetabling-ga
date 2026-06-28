import logging

from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.student import Student
from src.models.timeslot import Timeslot

logger = logging.getLogger(__name__)


def validate_dataset(
    students: list[Student],
    courses: list[Course],
    enrollments: list[Enrollment],
    timeslots: list[Timeslot],
) -> bool:
    """Validate that the dataset satisfies all required consistency checks.

    Checks:
    - Unique student IDs.
    - Unique course IDs.
    - Reference integrity: enrollments refer to valid students and courses.
    - Timeslots count is >= 1.
    - No empty strings in ID fields.
    - Semesters, days, sessions must be positive integers.

    Args:
        students: Loaded list of Student objects.
        courses: Loaded list of Course objects.
        enrollments: Loaded list of Enrollment objects.
        timeslots: Loaded list of Timeslot objects.

    Returns:
        True if the dataset is completely valid.

    Raises:
        ValueError: If any validation rule is violated.
    """
    # 1. Validate timeslots existence
    if not timeslots:
        raise ValueError("Dataset is invalid: No timeslots defined.")

    # 2. Check student IDs
    student_ids = set()
    for student in students:
        if not student.student_id:
            raise ValueError("Student record has an empty student_id.")
        if student.student_id in student_ids:
            raise ValueError(f"Duplicate student_id found: {student.student_id}")
        if student.current_semester <= 0:
            raise ValueError(
                f"Invalid semester {student.current_semester} for "
                f"student {student.student_id}."
            )
        student_ids.add(student.student_id)

    # 3. Check course IDs
    course_ids = set()
    for course in courses:
        if not course.course_id:
            raise ValueError("Course record has an empty course_id.")
        if course.course_id in course_ids:
            raise ValueError(f"Duplicate course_id found: {course.course_id}")
        if course.offered_semester <= 0:
            raise ValueError(
                f"Invalid offered semester {course.offered_semester} for "
                f"course {course.course_id}."
            )
        course_ids.add(course.course_id)

    # 4. Check timeslot fields
    slot_ids = set()
    for slot in timeslots:
        if slot.slot_id in slot_ids:
            raise ValueError(f"Duplicate slot_id found: {slot.slot_id}")
        if slot.day <= 0:
            raise ValueError(f"Invalid day {slot.day} in timeslot {slot.slot_id}.")
        if slot.session <= 0:
            raise ValueError(
                f"Invalid session {slot.session} in timeslot {slot.slot_id}."
            )
        slot_ids.add(slot.slot_id)

    # 5. Check enrollment reference integrity
    for idx, enrollment in enumerate(enrollments, start=1):
        if enrollment.student_id not in student_ids:
            raise ValueError(
                f"Enrollment at row {idx} refers to non-existent student: "
                f"{enrollment.student_id}"
            )
        if enrollment.course_id not in course_ids:
            raise ValueError(
                f"Enrollment at row {idx} refers to non-existent course: "
                f"{enrollment.course_id}"
            )

    logger.info("Dataset validation passed successfully.")
    return True
