import tempfile
from pathlib import Path

import pytest

from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.student import Student
from src.models.timeslot import Timeslot
from src.preprocessing.conflict_matrix import build_conflict_matrix
from src.preprocessing.load_dataset import (
    load_dataset,
)
from src.preprocessing.validator import validate_dataset


@pytest.fixture
def temp_csv_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_load_and_validate_dataset(temp_csv_dir):
    # Create valid dummy CSV files
    students_data = (
        "student_id,faculty_id,department_id,current_semester\n"
        "S1,FMIPA,IF,4\nS2,FMIPA,IF,4\n"
    )
    courses_data = (
        "course_id,course_name,faculty_id,department_id,"
        "offered_semester,course_type\n"
        "C1,Calculus,FMIPA,IF,1,DEPARTMENT\n"
        "C2,Structures,FMIPA,IF,3,DEPARTMENT\n"
    )
    enrollment_data = "student_id,course_id\nS1,C1\nS1,C2\nS2,C1\n"
    timeslots_data = "slot_id,day,session\n1,1,1\n2,1,2\n"

    with open(temp_csv_dir / "students.csv", "w", encoding="utf-8") as f:
        f.write(students_data)
    with open(temp_csv_dir / "courses.csv", "w", encoding="utf-8") as f:
        f.write(courses_data)
    with open(temp_csv_dir / "enrollment.csv", "w", encoding="utf-8") as f:
        f.write(enrollment_data)
    with open(temp_csv_dir / "timeslots.csv", "w", encoding="utf-8") as f:
        f.write(timeslots_data)

    # Create empty placeholder CSVs for rooms and slot_blocks
    with open(temp_csv_dir / "rooms.csv", "w", encoding="utf-8") as f:
        f.write("room_id,capacity\n")
    with open(temp_csv_dir / "slot_blocks.csv", "w", encoding="utf-8") as f:
        f.write("faculty_id,day,session\n")

    # Test load with new signature
    students, courses, enrollments, timeslots, rooms, slot_blocks = load_dataset(
        temp_csv_dir
    )

    assert len(students) == 2
    assert students[0].student_id == "S1"
    assert students[0].current_semester == 4

    assert len(courses) == 2
    assert courses[0].course_id == "C1"
    assert courses[0].offered_semester == 1

    assert len(enrollments) == 3
    assert len(timeslots) == 2

    # Test validator
    assert validate_dataset(students, courses, enrollments, timeslots) is True


def test_validator_fails_duplicate_student_id():
    students = [
        Student("S1", "FMIPA", "IF", 1),
        Student("S1", "FMIPA", "IF", 2),
    ]
    courses = [Course("C1", "Calculus", "FMIPA", "IF", 1, "DEPARTMENT")]
    enrollments = [Enrollment("S1", "C1")]
    timeslots = [Timeslot(1, 1, 1)]

    with pytest.raises(ValueError, match="Duplicate student_id found"):
        validate_dataset(students, courses, enrollments, timeslots)


def test_validator_fails_missing_enrollment_course():
    students = [Student("S1", "FMIPA", "IF", 1)]
    courses = [Course("C1", "Calculus", "FMIPA", "IF", 1, "DEPARTMENT")]
    # Enrollment C2 doesn't exist in courses
    enrollments = [Enrollment("S1", "C2")]
    timeslots = [Timeslot(1, 1, 1)]

    with pytest.raises(ValueError, match="refers to non-existent course"):
        validate_dataset(students, courses, enrollments, timeslots)


def test_build_conflict_matrix():
    courses = [
        Course("C1", "Calculus", "FMIPA", "IF", 1, "DEPARTMENT"),
        Course("C2", "Structures", "FMIPA", "IF", 3, "DEPARTMENT"),
        Course("C3", "Isolated", "FMIPA", "IF", 3, "DEPARTMENT"),
    ]
    enrollments = [
        Enrollment("S1", "C1"),
        Enrollment("S1", "C2"),
        Enrollment("S2", "C1"),
    ]

    matrix = build_conflict_matrix(enrollments, courses)

    # C1 and C2 should conflict since S1 is enrolled in both
    assert "C2" in matrix["C1"]
    assert "C1" in matrix["C2"]

    # C3 is isolated and should have an empty set
    assert matrix["C3"] == set()
