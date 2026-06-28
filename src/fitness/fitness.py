from collections import Counter, defaultdict

from src.fitness.hard_constraints import count_hard_constraint_violations
from src.fitness.soft_constraints import (
    calculate_consecutive_and_too_many,
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
    WEIGHT_HARD_CONSTRAINT,
    WEIGHT_HIGH_ENROLLMENT_SEPARATION,
    WEIGHT_PREFERRED_GAP,
    WEIGHT_SAME_SEMESTER_SEPARATION,
    WEIGHT_SPREAD_PENALTY,
    WEIGHT_TOO_MANY_EXAMS,
)

# Global caches for optimization
_timeslot_map: dict[int, tuple[int, int]] = {}
_student_courses: dict[str, list[str]] = {}
_course_indices: dict[str, int] = {}
_dept_sem_cores: dict[tuple[str, int], list[str]] = {}
_high_enrollment_courses: set[str] = set()
_num_timeslots: int = 15


def set_timeslot_data(timeslots: list[Timeslot]) -> None:
    """Register timeslot mapping in the fitness module cache.

    Args:
        timeslots: List of Timeslot objects.
    """
    global _timeslot_map, _num_timeslots
    _timeslot_map = {t.slot_id: (t.day, t.session) for t in timeslots}
    _num_timeslots = len(timeslots) if timeslots else 15


def set_course_data(courses: list[Course]) -> None:
    """Register course mappings in the fitness module cache.

    Args:
        courses: List of Course objects.
    """
    global _course_indices, _dept_sem_cores, _high_enrollment_courses
    _course_indices = {c.course_id: idx for idx, c in enumerate(courses)}

    # Group core department courses by (department, offered_semester)
    _dept_sem_cores = defaultdict(list)
    for c in courses:
        if c.course_type == "DEPARTMENT":
            key = (c.department_id, c.offered_semester)
            _dept_sem_cores[key].append(c.course_id)

        # General courses are always marked as high enrollment
        if c.course_type == "GENERAL":
            _high_enrollment_courses.add(c.course_id)


def set_student_data(students: list[Student], enrollments: list[Enrollment]) -> None:
    """Register student courses and thresholds in the fitness module cache.

    Args:
        students: List of Student objects.
        enrollments: List of Enrollment objects.
    """
    global _student_courses, _high_enrollment_courses
    _student_courses = defaultdict(list)
    for e in enrollments:
        _student_courses[e.student_id].append(e.course_id)

    # Count enrollments per course to flag courses exceeding HIGH_ENROLLMENT_THRESHOLD
    course_counts = Counter(e.course_id for e in enrollments)
    for cid, count in course_counts.items():
        if count >= HIGH_ENROLLMENT_THRESHOLD:
            _high_enrollment_courses.add(cid)


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
    conflict_matrix: ConflictMatrix,
    timeslots: list[int],
) -> float:
    """Calculate the fitness of a chromosome.

    Fitness is represented as the total penalty value where lower is better.

    Args:
        chromosome: Candidate solution (list of timeslots assigned to each course).
        conflict_matrix: Adjacency list of course conflicts.
        timeslots: List of available timeslot IDs.

    Returns:
        float: The calculated total penalty.
    """
    # 1. Hard constraints
    hc_violations = count_hard_constraint_violations(
        chromosome, _student_courses, _course_indices
    )

    # 2. Soft constraints
    consecutive_val, too_many_val, pref_gap_val = calculate_consecutive_and_too_many(
        chromosome, _student_courses, _course_indices, _timeslot_map
    )

    spread_val = calculate_spread_penalty(chromosome, _num_timeslots)

    same_sem_val = calculate_same_semester_separation(
        chromosome, _course_indices, _timeslot_map, _dept_sem_cores
    )

    high_enroll_val = calculate_high_enrollment_separation(
        chromosome, _course_indices, _timeslot_map, _high_enrollment_courses
    )

    # 3. Sum penalties weighted
    total_penalty = (
        hc_violations * WEIGHT_HARD_CONSTRAINT
        + consecutive_val * WEIGHT_CONSECUTIVE_EXAMS
        + too_many_val * WEIGHT_TOO_MANY_EXAMS
        + spread_val * WEIGHT_SPREAD_PENALTY
        + same_sem_val * WEIGHT_SAME_SEMESTER_SEPARATION
        + high_enroll_val * WEIGHT_HIGH_ENROLLMENT_SEPARATION
        + pref_gap_val * WEIGHT_PREFERRED_GAP
    )

    return total_penalty


def calculate_penalty(
    chromosome: Chromosome,
    conflict_matrix: ConflictMatrix,
    timeslots: list[int],
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
    hc = count_hard_constraint_violations(chromosome, _student_courses, _course_indices)
    consecutive, too_many, pref_gap = calculate_consecutive_and_too_many(
        chromosome, _student_courses, _course_indices, _timeslot_map
    )
    spread = calculate_spread_penalty(chromosome, _num_timeslots)
    same_sem = calculate_same_semester_separation(
        chromosome, _course_indices, _timeslot_map, _dept_sem_cores
    )
    high_enroll = calculate_high_enrollment_separation(
        chromosome, _course_indices, _timeslot_map, _high_enrollment_courses
    )

    return {
        "hard_constraint_violations": hc,
        "consecutive_exams_violations": consecutive,
        "too_many_exams_violations": too_many,
        "preferred_gap_violations": pref_gap,
        "spread_penalty": spread,
        "same_semester_violations": same_sem,
        "high_enrollment_violations": high_enroll,
        "total_penalty": (
            hc * WEIGHT_HARD_CONSTRAINT
            + consecutive * WEIGHT_CONSECUTIVE_EXAMS
            + too_many * WEIGHT_TOO_MANY_EXAMS
            + spread * WEIGHT_SPREAD_PENALTY
            + same_sem * WEIGHT_SAME_SEMESTER_SEPARATION
            + high_enroll * WEIGHT_HIGH_ENROLLMENT_SEPARATION
            + pref_gap * WEIGHT_PREFERRED_GAP
        ),
    }
