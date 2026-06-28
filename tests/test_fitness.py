import pytest

from src.fitness.fitness import (
    evaluate_constraints,
    initialize_fitness_data,
)
from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.student import Student
from src.models.timeslot import Timeslot


@pytest.fixture(autouse=True)
def setup_fitness_data():
    # Setup standard IPB-style courses, students, enrollments, and timeslots
    courses = [
        # General (high enrollment if taken by enough students, or by type)
        Course("GEN101", "Pancasila", "GENERAL", "GENERAL", 1, "GENERAL"),
        Course("GEN102", "Agama", "GENERAL", "GENERAL", 2, "GENERAL"),
        # Department core
        Course("KOM201", "Pemrograman", "FMIPA", "ILKOM", 2, "DEPARTMENT"),
        Course("KOM202", "PBO", "FMIPA", "ILKOM", 2, "DEPARTMENT"),
        Course("STT201", "Metode Stat", "FMIPA", "STAT", 2, "DEPARTMENT"),
    ]

    timeslots = [
        Timeslot(1, 1, 1),  # Day 1 Session 1
        Timeslot(2, 1, 2),  # Day 1 Session 2
        Timeslot(3, 1, 3),  # Day 1 Session 3
        Timeslot(4, 2, 1),  # Day 2 Session 1
        Timeslot(5, 2, 2),  # Day 2 Session 2
        Timeslot(6, 5, 3),  # Day 5 Session 3 (Friday Afternoon)
    ]

    students = [
        Student("S1", "FMIPA", "ILKOM", 2),
        Student("S2", "FMIPA", "STAT", 2),
    ]

    enrollments = [
        # Student 1 takes general and department cores
        Enrollment("S1", "GEN101"),
        Enrollment("S1", "KOM201"),
        Enrollment("S1", "KOM202"),
        # Student 2 takes general and stat
        Enrollment("S2", "GEN101"),
        Enrollment("S2", "STT201"),
    ]

    initialize_fitness_data(students, courses, enrollments, timeslots)


def test_zero_violation_schedule():
    # Chromosome maps: GEN101, GEN102, KOM201, KOM202, STT201
    # We map them to widely spread slots:
    # GEN101 -> Slot 1 (Day 1 Session 1)
    # GEN102 -> Slot 4 (Day 2 Session 1)
    # KOM201 -> Slot 5 (Day 2 Session 2)
    # KOM202 -> Slot 3 (Day 1 Session 3)
    # STT201 -> Slot 4 (Day 2 Session 1)
    chromosome = [1, 4, 5, 3, 4]

    stats = evaluate_constraints(chromosome)
    assert stats["hard_constraint_violations"] == 0
    assert stats["consecutive_exams_violations"] == 0


def test_hard_constraint_violation():
    # S1 takes GEN101 and KOM201. Placing both in slot 1 causes a clash.
    chromosome = [1, 4, 1, 3, 5]
    stats = evaluate_constraints(chromosome)
    assert stats["hard_constraint_violations"] >= 1


def test_consecutive_exams_violation():
    # S1 takes GEN101 (slot 1) and KOM201 (slot 2). Adjacency causes consecutive violation.
    # S2 takes GEN101 (slot 1) and STT201 (slot 3). Gap causes preferred gap violation.
    chromosome = [1, 4, 2, 5, 3]
    stats = evaluate_constraints(chromosome)
    assert stats["consecutive_exams_violations"] >= 1
    assert stats["preferred_gap_violations"] == 1


def test_same_semester_core_separation_violation():
    # KOM201 and KOM202 are core courses in the same semester.
    # Scheduled on Day 1 Session 1 and Day 1 Session 2. Same day causes violation.
    chromosome = [4, 5, 1, 2, 3]
    stats = evaluate_constraints(chromosome)
    assert stats["same_semester_violations"] >= 1


def test_greedy_baseline():
    from src.evaluation.greedy import run_greedy
    from src.preprocessing.conflict_matrix import build_conflict_matrix

    courses = [
        Course("GEN101", "Pancasila", "GENERAL", "GENERAL", 1, "GENERAL"),
        Course("GEN102", "Agama", "GENERAL", "GENERAL", 2, "GENERAL"),
        Course("KOM201", "Pemrograman", "FMIPA", "ILKOM", 2, "DEPARTMENT"),
        Course("KOM202", "PBO", "FMIPA", "ILKOM", 2, "DEPARTMENT"),
        Course("STT201", "Metode Stat", "FMIPA", "STAT", 2, "DEPARTMENT"),
    ]
    timeslots = [
        Timeslot(1, 1, 1),
        Timeslot(2, 1, 2),
        Timeslot(3, 1, 3),
        Timeslot(4, 2, 1),
        Timeslot(5, 2, 2),
    ]
    students = [
        Student("S1", "FMIPA", "ILKOM", 2),
        Student("S2", "FMIPA", "STAT", 2),
    ]
    enrollments = [
        Enrollment("S1", "GEN101"),
        Enrollment("S1", "KOM201"),
        Enrollment("S1", "KOM202"),
        Enrollment("S2", "GEN101"),
        Enrollment("S2", "STT201"),
    ]

    conflict_matrix = build_conflict_matrix(enrollments, courses)
    result = run_greedy(students, courses, enrollments, timeslots, conflict_matrix)

    assert len(result.best_solution) == len(courses)
    assert result.best_fitness >= 0


def test_preferred_gap_violation():
    # S1 takes GEN101 (slot 1) and KOM201 (slot 3). Gap session 2 is empty.
    # KOM202 is placed in slot 4 (Day 2) so S1 only has sessions 1 and 3 on Day 1.
    # This should trigger preferred gap violation, but NOT consecutive exams.
    chromosome = [1, 4, 3, 4, 4]
    stats = evaluate_constraints(chromosome)
    assert stats["preferred_gap_violations"] >= 1
    assert stats["consecutive_exams_violations"] == 0


def test_friday_afternoon_penalty():
    # Map GEN101 to slot 6 (Friday Session 3)
    # This should trigger Friday afternoon penalty.
    chromosome = [6, 4, 5, 3, 4]
    stats = evaluate_constraints(chromosome)
    assert stats["friday_afternoon_violations"] == 1
    # Check that total penalty includes Friday Afternoon weight (5.0)
    assert stats["total_penalty"] >= 5.0
