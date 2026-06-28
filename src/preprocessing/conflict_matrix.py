import itertools
from collections import defaultdict

from src.ga.chromosome import ConflictMatrix
from src.models.course import Course
from src.models.enrollment import Enrollment


def build_conflict_matrix(
    enrollments: list[Enrollment],
    courses: list[Course],
) -> ConflictMatrix:
    """Build the conflict matrix representing shared students between courses.

    Two courses are in conflict (have an edge between them) if at least
    one student is enrolled in both courses.

    All courses must have an entry in the returned dictionary, even if they
    have no conflicts (an empty set).

    Args:
        enrollments: List of Enrollment relations.
        courses: List of all Course dataclasses in the system.

    Returns:
        ConflictMatrix: A dictionary mapping each course ID to the set of
            course IDs it conflicts with.
    """
    # 1. Initialize for all courses to ensure isolated courses are present
    conflict_matrix: ConflictMatrix = {c.course_id: set() for c in courses}

    # 2. Group course enrollments by student
    student_courses = defaultdict(list)
    for enrollment in enrollments:
        student_courses[enrollment.student_id].append(enrollment.course_id)

    # 3. Add conflicts for each pair of courses a student is taking
    for courses_taken in student_courses.values():
        if len(courses_taken) < 2:
            continue
        # Use combinations to find all pairs (a, b)
        for a, b in itertools.combinations(courses_taken, 2):
            # Only add conflicts for known courses (handling edge cases)
            if a in conflict_matrix and b in conflict_matrix:
                conflict_matrix[a].add(b)
                conflict_matrix[b].add(a)

    return conflict_matrix
