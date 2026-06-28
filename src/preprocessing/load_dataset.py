import csv
from pathlib import Path

from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.student import Student
from src.models.timeslot import Timeslot


def load_students(path: Path) -> list[Student]:
    """Load students from a CSV file.

    Args:
        path: Path to the students CSV file.

    Returns:
        List of Student dataclasses.
    """
    if not path.exists():
        raise FileNotFoundError(f"Students file not found at: {path}")

    students = []
    required_cols = {"student_id", "faculty_id", "department_id", "current_semester"}

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"CSV file is empty: {path}")
            missing = required_cols - set(reader.fieldnames)
            if missing:
                raise ValueError(f"Missing required columns in students CSV: {missing}")
            for row_idx, row in enumerate(reader, start=2):
                try:
                    students.append(
                        Student(
                            student_id=row["student_id"].strip(),
                            faculty_id=row["faculty_id"].strip(),
                            department_id=row["department_id"].strip(),
                            current_semester=int(row["current_semester"]),
                        )
                    )
                except ValueError as e:
                    raise ValueError(
                        f"Invalid data at row {row_idx} of students CSV: {e}"
                    ) from e
    except Exception as e:
        if not isinstance(e, (FileNotFoundError, ValueError)):
            raise ValueError(f"Failed to parse students CSV: {e}") from e
        raise
    return students


def load_courses(path: Path) -> list[Course]:
    """Load courses from a CSV file.

    Args:
        path: Path to the courses CSV file.

    Returns:
        List of Course dataclasses.
    """
    if not path.exists():
        raise FileNotFoundError(f"Courses file not found at: {path}")

    courses = []
    required_cols = {
        "course_id",
        "course_name",
        "faculty_id",
        "department_id",
        "offered_semester",
        "course_type",
    }
    # Optional column room_id for room assignment

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"CSV file is empty: {path}")
            missing = required_cols - set(reader.fieldnames)
            if missing:
                raise ValueError(f"Missing required columns in courses CSV: {missing}")
            for row_idx, row in enumerate(reader, start=2):
                try:
                    courses.append(
                        Course(
                            course_id=row["course_id"].strip(),
                            course_name=row["course_name"].strip(),
                            faculty_id=row["faculty_id"].strip(),
                            department_id=row["department_id"].strip(),
                            offered_semester=int(row["offered_semester"]),
                            course_type=row["course_type"].strip(),
                            # If room_id column exists, include it; otherwise empty string
                            room_id=row.get("room_id", "").strip(),
                        )
                    )
                except ValueError as e:
                    raise ValueError(
                        f"Invalid data at row {row_idx} of courses CSV: {e}"
                    ) from e
    except Exception as e:
        if not isinstance(e, (FileNotFoundError, ValueError)):
            raise ValueError(f"Failed to parse courses CSV: {e}") from e
        raise
    return courses


def load_enrollments(path: Path) -> list[Enrollment]:
    """Load enrollments from a CSV file.

    Args:
        path: Path to the enrollment CSV file.

    Returns:
        List of Enrollment dataclasses.
    """
    if not path.exists():
        raise FileNotFoundError(f"Enrollment file not found at: {path}")

    enrollments = []
    required_cols = {"student_id", "course_id"}

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"CSV file is empty: {path}")
            missing = required_cols - set(reader.fieldnames)
            if missing:
                raise ValueError(
                    f"Missing required columns in enrollment CSV: {missing}"
                )
            for row in reader:
                enrollments.append(
                    Enrollment(
                        student_id=row["student_id"].strip(),
                        course_id=row["course_id"].strip(),
                    )
                )
    except Exception as e:
        if not isinstance(e, (FileNotFoundError, ValueError)):
            raise ValueError(f"Failed to parse enrollment CSV: {e}") from e
        raise
    return enrollments


def load_timeslots(path: Path) -> list[Timeslot]:
    """Load timeslots from a CSV file.

    Args:
        path: Path to the timeslots CSV file.

    Returns:
        List of Timeslot dataclasses.
    """
    if not path.exists():
        raise FileNotFoundError(f"Timeslots file not found at: {path}")

    timeslots = []
    required_cols = {"slot_id", "day", "session"}

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"CSV file is empty: {path}")
            missing = required_cols - set(reader.fieldnames)
            if missing:
                raise ValueError(
                    f"Missing required columns in timeslots CSV: {missing}"
                )
            for row_idx, row in enumerate(reader, start=2):
                try:
                    timeslots.append(
                        Timeslot(
                            slot_id=int(row["slot_id"]),
                            day=int(row["day"]),
                            session=int(row["session"]),
                        )
                    )
                except ValueError as e:
                    raise ValueError(
                        f"Invalid data at row {row_idx} of timeslots CSV: {e}"
                    ) from e
    except Exception as e:
        if not isinstance(e, (FileNotFoundError, ValueError)):
            raise ValueError(f"Failed to parse timeslots CSV: {e}") from e
        raise
    return timeslots


def load_rooms(path: Path) -> dict[str, int]:
    """Load room capacities from a CSV file.

    Expected columns: room_id,capacity
    Returns a mapping of room_id -> capacity. If file missing, returns empty dict.
    """
    if not path.exists():
        return {}
    rooms: dict[str, int] = {}
    required_cols = {"room_id", "capacity"}
    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"CSV file is empty: {path}")
            missing = required_cols - set(reader.fieldnames)
            if missing:
                raise ValueError(f"Missing required columns in rooms CSV: {missing}")
            for row in reader:
                room_id = row["room_id"].strip()
                capacity = int(row["capacity"])
                rooms[room_id] = capacity
    except Exception as e:
        raise ValueError(f"Failed to parse rooms CSV: {e}") from e
    return rooms


def load_slot_blocks(path: Path) -> set[tuple[str, int, int]]:
    """Load faculty slot block constraints.

    Expected columns: faculty_id,day,session
    Returns a set of (faculty_id, day, session) tuples. If file missing, returns empty set.
    """
    if not path.exists():
        return set()
    blocks: set[tuple[str, int, int]] = set()
    required_cols = {"faculty_id", "day", "session"}
    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"CSV file is empty: {path}")
            missing = required_cols - set(reader.fieldnames)
            if missing:
                raise ValueError(
                    f"Missing required columns in slot_blocks CSV: {missing}"
                )
            for row in reader:
                fac = row["faculty_id"].strip()
                day = int(row["day"])
                session = int(row["session"])
                blocks.add((fac, day, session))
    except Exception as e:
        raise ValueError(f"Failed to parse slot_blocks CSV: {e}") from e
    return blocks


def load_dataset(
    data_dir: Path,
) -> tuple[
    list[Student],
    list[Course],
    list[Enrollment],
    list[Timeslot],
    dict[str, int],
    set[tuple[str, int, int]],
]:
    """Load all scheduling data from a dataset directory.

    Args:
        data_dir: Directory containing the CSV files:
            students.csv, courses.csv, enrollment.csv, timeslots.csv,
            rooms.csv (optional), slot_blocks.csv (optional).

    Returns:
        A tuple of (students, courses, enrollments, timeslots, rooms, slot_blocks).
    """
    students = load_students(data_dir / "students.csv")
    courses = load_courses(data_dir / "courses.csv")
    enrollments = load_enrollments(data_dir / "enrollment.csv")
    timeslots = load_timeslots(data_dir / "timeslots.csv")
    rooms = load_rooms(data_dir / "rooms.csv")
    slot_blocks = load_slot_blocks(data_dir / "slot_blocks.csv")
    return students, courses, enrollments, timeslots, rooms, slot_blocks
