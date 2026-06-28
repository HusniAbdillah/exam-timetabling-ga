from collections import Counter, defaultdict

from src.fitness.additional_constraints import (
    max_exams_per_day_violations,
    room_capacity_violations,
    slot_block_violations,
)
from src.fitness.hard_constraints import count_hard_constraint_violations
from src.fitness.soft_constraints import (
    calculate_consecutive_and_too_many,
    calculate_friday_afternoon_penalty,
    calculate_high_enrollment_separation,
    calculate_same_semester_separation,
    calculate_spread_penalty,
)
from src.ga.chromosome import Chromosome, ConflictMatrix
from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.student import Student
from src.models.timeslot import Timeslot
from src.utils.constants import (
    HIGH_ENROLLMENT_THRESHOLD,
    WEIGHT_CONSECUTIVE_EXAMS,
    WEIGHT_FRIDAY_AFTERNOON_PENALTY,
    WEIGHT_HARD_CONSTRAINT,
    WEIGHT_HIGH_ENROLLMENT_SEPARATION,
    WEIGHT_MAX_EXAMS_PER_DAY,
    WEIGHT_PREFERRED_GAP,
    WEIGHT_ROOM_CAPACITY,
    WEIGHT_SAME_SEMESTER_SEPARATION,
    WEIGHT_SLOT_BLOCK,
    WEIGHT_SPREAD_PENALTY,
    WEIGHT_TOO_MANY_EXAMS,
)

# Global caches for optimization
_timeslot_map: dict[int, tuple[int, int]] = {}
_student_courses: dict[str, list[str]] = {}
_course_indices: dict[str, int] = {}
_dept_sem_cores: dict[tuple[str, int], list[str]] = {}
_high_enrollment_courses: set[str] = set()
_course_faculty_map: dict[str, str] = {}
_room_capacities: dict[str, int] = {}
_course_room_map: dict[str, str] = {}
_blocked_slots: set[tuple[str, int, int]] = set()
_num_timeslots: int = 15

# Optimized caches with integer indices
_student_course_indices: dict[str, list[int]] = {}
_dept_sem_core_indices: dict[tuple[str, int], list[int]] = {}
_high_enrollment_course_indices: set[int] = set()
_course_enrollments: dict[str, int] = {}
_course_faculty_indices: dict[int, str] = {}


def set_timeslot_data(timeslots: list[Timeslot]) -> None:
    """Register timeslot mapping in the fitness module cache.

    Args:
        timeslots: List of Timeslot objects.
    """
    global _timeslot_map, _num_timeslots
    _timeslot_map = {t.slot_id: (t.day, t.session) for t in timeslots}
    _num_timeslots = len(timeslots) if timeslots else 15


def set_course_data(courses: list[Course]) -> None:
    """Register course mappings and faculty information in the fitness module cache.

    Args:
        courses: List of Course objects.
    """
    global \
        _course_indices, \
        _dept_sem_cores, \
        _high_enrollment_courses, \
        _course_faculty_map, \
        _course_room_map, \
        _course_faculty_indices
    _course_indices = {c.course_id: idx for idx, c in enumerate(courses)}
    _dept_sem_cores = defaultdict(list)
    _course_faculty_map = {}
    _course_room_map = {}
    _course_faculty_indices = {}
    for idx, c in enumerate(courses):
        _course_faculty_map[c.course_id] = c.faculty_id
        _course_faculty_indices[idx] = c.faculty_id
        if c.course_type == "DEPARTMENT":
            key = (c.department_id, c.offered_semester)
            _dept_sem_cores[key].append(c.course_id)
        if c.course_type == "GENERAL":
            _high_enrollment_courses.add(c.course_id)


def set_student_data(students: list[Student], enrollments: list[Enrollment]) -> None:
    """Register student courses and high enrollment courses based on enrollment counts.

    Args:
        students: List of Student objects.
        enrollments: List of Enrollment objects.
    """
    global \
        _student_courses, \
        _high_enrollment_courses, \
        _course_enrollments, \
        _student_course_indices, \
        _high_enrollment_course_indices, \
        _dept_sem_core_indices
    _student_courses = defaultdict(list)
    for e in enrollments:
        _student_courses[e.student_id].append(e.course_id)

    # Flag high‑enrollment courses based on threshold
    _course_enrollments = Counter(e.course_id for e in enrollments)
    for cid, count in _course_enrollments.items():
        if count >= HIGH_ENROLLMENT_THRESHOLD:
            _high_enrollment_courses.add(cid)

    # Populate optimized integer course index caches
    _student_course_indices = {}
    for sid, cids in _student_courses.items():
        _student_course_indices[sid] = [
            _course_indices[cid] for cid in cids if cid in _course_indices
        ]

    _high_enrollment_course_indices = {
        _course_indices[cid]
        for cid in _high_enrollment_courses
        if cid in _course_indices
    }

    _dept_sem_core_indices = {}
    for key, cids in _dept_sem_cores.items():
        _dept_sem_core_indices[key] = [
            _course_indices[cid] for cid in cids if cid in _course_indices
        ]


def set_room_data(
    room_cap_dict: dict[str, int],
    course_room_dict: dict[str, str],
) -> None:
    """Register room capacities and course‑to‑room assignments.

    Args:
        room_cap_dict: Mapping from room_id to its capacity.
        course_room_dict: Mapping from course_id to assigned room_id.
    """
    global _room_capacities, _course_room_map
    _room_capacities = room_cap_dict
    _course_room_map = course_room_dict


def set_blocked_slots(blocked: set[tuple[str, int, int]]) -> None:
    """Register faculty slot block constraints.

    Args:
        blocked: Set of (faculty_id, day, session) tuples.
    """
    global _blocked_slots
    _blocked_slots = blocked


def initialize_fitness_data(
    students: list[Student],
    courses: list[Course],
    enrollments: list[Enrollment],
    timeslots: list[Timeslot],
) -> None:
    """Helper function to initialize all caches at once.

    Args:
        students: List of Student objects.
        courses: List of Course objects.
        enrollments: List of Enrollment objects.
        timeslots: List of Timeslot objects.
    """
    set_timeslot_data(timeslots)
    set_course_data(courses)
    set_student_data(students, enrollments)


def calculate_fitness(
    chromosome: Chromosome,
    conflict_matrix: ConflictMatrix | None = None,
    timeslots: list[int] | None = None,
) -> float:
    """Calculate the fitness of a chromosome.

    Fitness is represented as the total penalty value where lower is better.

    Args:
        chromosome: Candidate solution (list of timeslots assigned to each course).
        conflict_matrix: Adjacency list of course conflicts (unused).
        timeslots: List of available timeslot IDs (unused).

    Returns:
        float: The calculated total penalty.
    """
    # Hard constraints
    hc_violations = count_hard_constraint_violations(
        chromosome, _student_course_indices
    )
    max_exams_per_day_val = max_exams_per_day_violations(
        chromosome, _student_course_indices, _timeslot_map
    )
    # Room capacity and slot block violations (if data provided)
    room_cap_viol = 0
    slot_block_viol = 0
    if _room_capacities and _course_room_map:
        room_cap_viol = room_capacity_violations(
            chromosome,
            _course_indices,
            _timeslot_map,
            _course_room_map,
            _room_capacities,
        )
    if _blocked_slots:
        slot_block_viol = slot_block_violations(
            chromosome,
            _timeslot_map,
            _course_faculty_indices,
            _blocked_slots,
        )
    # Soft constraints
    consecutive_val, too_many_val, pref_gap_val = calculate_consecutive_and_too_many(
        chromosome, _student_course_indices, _timeslot_map
    )
    spread_val = calculate_spread_penalty(chromosome, _num_timeslots)
    same_sem_val = calculate_same_semester_separation(
        chromosome, _timeslot_map, _dept_sem_core_indices
    )
    high_enroll_val = calculate_high_enrollment_separation(
        chromosome, _timeslot_map, _high_enrollment_course_indices
    )
    friday_afternoon_val = calculate_friday_afternoon_penalty(chromosome, _timeslot_map)
    # Weighted sum
    total_penalty = (
        hc_violations * WEIGHT_HARD_CONSTRAINT
        + consecutive_val * WEIGHT_CONSECUTIVE_EXAMS
        + too_many_val * WEIGHT_TOO_MANY_EXAMS
        + spread_val * WEIGHT_SPREAD_PENALTY
        + same_sem_val * WEIGHT_SAME_SEMESTER_SEPARATION
        + high_enroll_val * WEIGHT_HIGH_ENROLLMENT_SEPARATION
        + pref_gap_val * WEIGHT_PREFERRED_GAP
        + friday_afternoon_val * WEIGHT_FRIDAY_AFTERNOON_PENALTY
        + max_exams_per_day_val * WEIGHT_MAX_EXAMS_PER_DAY
        + room_cap_viol * WEIGHT_ROOM_CAPACITY
        + slot_block_viol * WEIGHT_SLOT_BLOCK
    )
    return total_penalty


def calculate_penalty(
    chromosome: Chromosome,
    conflict_matrix: ConflictMatrix | None = None,
    timeslots: list[int] | None = None,
) -> float:
    """Alias for calculate_fitness.

    Args:
        chromosome: Candidate solution.
        conflict_matrix: Adjacency list of course conflicts.
        timeslots: List of available timeslots.

    Returns:
        Total penalty value.
    """
    return calculate_fitness(chromosome, conflict_matrix, timeslots)


def evaluate_constraints(chromosome: Chromosome) -> dict[str, float | int]:
    """Exposes details of all constraint violations for stats and reporting.

    Args:
        chromosome: Candidate solution.

    Returns:
        dict: Summary of violations and sub-penalties.
    """
    hc = count_hard_constraint_violations(chromosome, _student_course_indices)
    consecutive, too_many, pref_gap = calculate_consecutive_and_too_many(
        chromosome, _student_course_indices, _timeslot_map
    )
    spread = calculate_spread_penalty(chromosome, _num_timeslots)
    same_sem = calculate_same_semester_separation(
        chromosome, _timeslot_map, _dept_sem_core_indices
    )
    high_enroll = calculate_high_enrollment_separation(
        chromosome, _timeslot_map, _high_enrollment_course_indices
    )
    friday_afternoon = calculate_friday_afternoon_penalty(chromosome, _timeslot_map)
    max_exams = max_exams_per_day_violations(
        chromosome, _student_course_indices, _timeslot_map
    )
    room_cap_viol = (
        room_capacity_violations(
            chromosome,
            _course_indices,
            _timeslot_map,
            _course_room_map,
            _room_capacities,
        )
        if _room_capacities and _course_room_map
        else 0
    )
    slot_block_viol = (
        slot_block_violations(
            chromosome, _timeslot_map, _course_faculty_indices, _blocked_slots
        )
        if _blocked_slots
        else 0
    )
    return {
        "hard_constraint_violations": hc,
        "consecutive_exams_violations": consecutive,
        "too_many_exams_violations": too_many,
        "preferred_gap_violations": pref_gap,
        "spread_penalty": spread,
        "same_semester_violations": same_sem,
        "high_enrollment_violations": high_enroll,
        "friday_afternoon_violations": friday_afternoon,
        "max_exams_per_day_violations": max_exams,
        "room_capacity_violations": room_cap_viol,
        "slot_block_violations": slot_block_viol,
        "total_penalty": (
            hc * WEIGHT_HARD_CONSTRAINT
            + consecutive * WEIGHT_CONSECUTIVE_EXAMS
            + too_many * WEIGHT_TOO_MANY_EXAMS
            + spread * WEIGHT_SPREAD_PENALTY
            + same_sem * WEIGHT_SAME_SEMESTER_SEPARATION
            + high_enroll * WEIGHT_HIGH_ENROLLMENT_SEPARATION
            + pref_gap * WEIGHT_PREFERRED_GAP
            + friday_afternoon * WEIGHT_FRIDAY_AFTERNOON_PENALTY
            + max_exams * WEIGHT_MAX_EXAMS_PER_DAY
            + room_cap_viol * WEIGHT_ROOM_CAPACITY
            + slot_block_viol * WEIGHT_SLOT_BLOCK
        ),
    }
