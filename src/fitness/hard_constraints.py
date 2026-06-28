from collections import Counter

from src.ga.chromosome import Chromosome


def count_hard_constraint_violations(
    chromosome: Chromosome,
    student_course_indices: dict[str, list[int]],
) -> int:
    """Calculate the number of hard constraint violations (student exam clashes).

    A violation occurs when a student is enrolled in multiple courses that
    are scheduled in the same timeslot.

    Args:
        chromosome: Candidate solution mapping course index to slot ID.
        student_course_indices: Mapping from student ID to list of course indices.

    Returns:
        Total number of student exam clashes (pairs of overlapping exams).
    """
    violations = 0
    for indices in student_course_indices.values():
        slots = []
        for idx in indices:
            slots.append(chromosome[idx])

        if len(slots) < 2:
            continue

        slot_counts = Counter(slots)
        for count in slot_counts.values():
            if count > 1:
                # Number of overlapping exam pairs for this student
                violations += count * (count - 1) // 2

    return violations
