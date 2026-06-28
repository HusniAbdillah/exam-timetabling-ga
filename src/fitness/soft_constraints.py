import itertools
from collections import Counter, defaultdict

from src.ga.chromosome import Chromosome


def calculate_consecutive_and_too_many(
    chromosome: Chromosome,
    student_course_indices: dict[str, list[int]],
    timeslot_map: dict[int, tuple[int, int]],
) -> tuple[int, int, int]:
    """Calculate consecutive exams, too many exams, and preferred gap violations.

    Args:
        chromosome: Candidate solution mapping course index to slot ID.
        student_course_indices: Mapping from student ID to list of course indices.
        timeslot_map: Mapping from slot ID to (day, session).

    Returns:
        A tuple of (consecutive, too_many, preferred_gap) violations.
    """
    consecutive = 0
    too_many = 0
    pref_gap = 0

    for indices in student_course_indices.values():
        # Get (day, session) for each course the student is taking
        student_slots = []
        for idx in indices:
            slot_id = chromosome[idx]
            if slot_id in timeslot_map:
                student_slots.append(timeslot_map[slot_id])

        if not student_slots:
            continue

        # Group by day
        day_sessions = defaultdict(list)
        for day, session in student_slots:
            day_sessions[day].append(session)

        # Evaluate constraints per day
        for sessions in day_sessions.values():
            # 1. Too Many Exams Per Day (> 2)
            if len(sessions) > 2:
                too_many += 1

            # 2. Consecutive Exams
            if len(sessions) >= 2:
                # Sort sessions to check adjacency
                sorted_sessions = sorted(sessions)
                for i in range(len(sorted_sessions) - 1):
                    if sorted_sessions[i + 1] - sorted_sessions[i] == 1:
                        consecutive += 1

            # 3. Preferred Gap (SIMAK IPB Style: Session 1 and 3 scheduled, but not Session 2)
            sessions_set = set(sessions)
            if 1 in sessions_set and 3 in sessions_set and 2 not in sessions_set:
                pref_gap += 1

    return consecutive, too_many, pref_gap


def calculate_spread_penalty(
    chromosome: Chromosome,
    num_timeslots: int,
) -> float:
    """Calculate the spread penalty of all scheduled exams.

    This measures how unevenly distributed exams are across timeslots using
    the variance of exam counts per slot.

    Args:
        chromosome: Candidate solution mapping course index to slot ID.
        num_timeslots: Total number of available timeslots.

    Returns:
        Variance of the number of courses scheduled per timeslot.
    """
    if not chromosome:
        return 0.0

    counts = Counter(chromosome)
    # Ensure all slots are accounted for
    all_counts = [counts.get(slot, 0) for slot in range(1, num_timeslots + 1)]

    mean = sum(all_counts) / num_timeslots
    variance = sum((c - mean) ** 2 for c in all_counts) / num_timeslots
    return variance


def calculate_same_semester_separation(
    chromosome: Chromosome,
    timeslot_map: dict[int, tuple[int, int]],
    dept_sem_core_indices: dict[tuple[str, int], list[int]],
) -> int:
    """Calculate penalty when department core courses of the same semester are close.

    Penalty is added if two core courses from the same department and semester
    are scheduled on the same day or on consecutive days.

    Args:
        chromosome: Candidate solution mapping course index to slot ID.
        timeslot_map: Mapping from slot ID to (day, session).
        dept_sem_core_indices: Mapping from (dept_id, semester) to list of core course indices.

    Returns:
        Total same semester core separation violations.
    """
    violations = 0

    for indices in dept_sem_core_indices.values():
        if len(indices) < 2:
            continue

        # Get days for these courses
        days = []
        for idx in indices:
            slot_id = chromosome[idx]
            if slot_id in timeslot_map:
                days.append(timeslot_map[slot_id][0])

        if len(days) < 2:
            continue

        # Check every pair of courses
        for d1, d2 in itertools.combinations(days, 2):
            if d1 == d2 or abs(d1 - d2) == 1:
                violations += 1

    return violations


def calculate_high_enrollment_separation(
    chromosome: Chromosome,
    timeslot_map: dict[int, tuple[int, int]],
    high_enrollment_course_indices: set[int],
) -> int:
    """Calculate penalty when multiple high enrollment exams are on the same day.

    Args:
        chromosome: Candidate solution mapping course index to slot ID.
        timeslot_map: Mapping from slot ID to (day, session).
        high_enrollment_course_indices: Set of course indices with high student enrollment.

    Returns:
        Total high enrollment separation violations.
    """
    violations = 0
    days = []

    for idx in high_enrollment_course_indices:
        slot_id = chromosome[idx]
        if slot_id in timeslot_map:
            days.append(timeslot_map[slot_id][0])

    if len(days) < 2:
        return 0

    # Count occurrences of high enrollment exams on the same day
    day_counts = Counter(days)
    for count in day_counts.values():
        if count > 1:
            # Overlapping pairs on the same day
            violations += count * (count - 1) // 2

    return violations


def calculate_friday_afternoon_penalty(
    chromosome: Chromosome,
    timeslot_map: dict[int, tuple[int, int]],
) -> int:
    """Calculate Friday afternoon penalty.

    A penalty is added for each exam scheduled on Friday (day 5)
    in Session 3 (afternoon).

    Args:
        chromosome: Candidate solution mapping course index to slot ID.
        timeslot_map: Mapping from slot ID to (day, session).

    Returns:
        Total Friday afternoon penalty violations.
    """
    violations = 0
    for slot_id in chromosome:
        if slot_id in timeslot_map:
            day, session = timeslot_map[slot_id]
            if day == 5 and session == 3:
                violations += 1
    return violations
