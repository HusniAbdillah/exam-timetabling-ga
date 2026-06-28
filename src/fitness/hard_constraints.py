from collections import Counter

from src.ga.chromosome import Chromosome


def count_hard_constraint_violations(
    chromosome: Chromosome,
    student_courses: dict[str, list[str]],
    course_indices: dict[str, int],
) -> int:
    """Calculate the number of hard constraint violations (student exam clashes).

    A violation occurs when a student is enrolled in multiple courses that
    are scheduled in the same timeslot.

    Args:
        chromosome: Candidate solution mapping course index to slot ID.
        student_courses: Mapping from student ID to list of course IDs they take.
        course_indices: Mapping from course ID to index in chromosome.

    Returns:
        Total number of student exam clashes (pairs of overlapping exams).
    """
    violations = 0
    for enrolled_courses in student_courses.values():
        slots = []
        for cid in enrolled_courses:
            if cid in course_indices:
                slots.append(chromosome[course_indices[cid]])

        if len(slots) < 2:
            continue

        slot_counts = Counter(slots)
        for count in slot_counts.values():
            if count > 1:
                # Number of overlapping exam pairs for this student
                violations += count * (count - 1) // 2

    return violations
