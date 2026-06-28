"""Additional hard constraints for the exam timetabling problem.

This module defines extra hard‑constraint functions that can be imported in
`src/fitness/fitness.py` and combined with the existing `count_hard_constraint_violations`
function.

The new constraint limits the number of exams a student may have on the same day.
It returns the **total number of excess exams** across all students (i.e. how many
exam slots need to be removed to satisfy the limit).
"""

from collections import defaultdict


def max_exams_per_day_violations(
    chromosome,
    student_course_indices,
    timeslot_map,
    max_exams_per_day: int = 2,
) -> int:
    """Count violations where a student has more than `max_exams_per_day` exams on a single day.

    Args:
        chromosome: List[int] – mapping `course_index -> timeslot_id`.
        student_course_indices: dict[student_id, list[course_index]].
        timeslot_map: dict[timeslot_id, (day, session)].
        max_exams_per_day: Maximum allowed exams per day for any student.

    Returns:
        int: Total number of excess exams across all students (penalty unit).
    """
    violations = 0
    for indices in student_course_indices.values():
        day_counts = defaultdict(int)
        for idx in indices:
            slot_id = chromosome[idx]
            day = timeslot_map[slot_id][0]
            day_counts[day] += 1
        for cnt in day_counts.values():
            if cnt > max_exams_per_day:
                violations += cnt - max_exams_per_day
    return violations


def room_capacity_violations(
    chromosome,
    course_indices,
    timeslot_map,
    course_room_map,
    room_capacities,
) -> int:
    """Calculate violations where total exam enrollment exceeds room capacities for each timeslot/room combination.

    Args:
        chromosome: List[int] – mapping course index to timeslot ID.
        course_indices: dict mapping course_id to index.
        timeslot_map: dict mapping timeslot_id to (day, session).
        course_room_map: dict mapping course_id to assigned room_id.
        room_capacities: dict mapping room_id to its integer capacity.
    Returns:
        int: Total excess seats across all timeslot-room combinations.
    """
    from src.fitness.fitness import _course_enrollments

    room_occupancy = defaultdict(int)
    for course_id, room_id in course_room_map.items():
        if course_id not in course_indices:
            continue
        idx = course_indices[course_id]
        slot_id = chromosome[idx]
        enrolled = _course_enrollments.get(course_id, 0)
        room_occupancy[(slot_id, room_id)] += enrolled

    violations = 0
    for (_slot_id, room_id), total_enrolled in room_occupancy.items():
        cap = room_capacities.get(room_id, 0)
        if total_enrolled > cap:
            violations += total_enrolled - cap
    return violations


def slot_block_violations(
    chromosome,
    timeslot_map,
    course_faculty_indices,
    blocked_slots,
) -> int:
    """Penalise exams scheduled in prohibited slots for a faculty.

    Args:
        chromosome: List[int] – mapping course index to timeslot ID.
        timeslot_map: dict mapping timeslot_id to (day, session).
        course_faculty_indices: dict mapping course index to faculty ID.
        blocked_slots: set of tuples (faculty_id, day, session) that are blocked.
    Returns:
        int: Number of exams violating the block.
    """
    violations = 0
    for idx, fac_id in course_faculty_indices.items():
        slot_id = chromosome[idx]
        day, session = timeslot_map[slot_id]
        if (fac_id, day, session) in blocked_slots:
            violations += 1
    return violations
