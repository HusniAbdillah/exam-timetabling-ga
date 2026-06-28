from pathlib import Path

# Paths
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

STUDENTS_CSV = DATA_DIR / "students.csv"
COURSES_CSV = DATA_DIR / "courses.csv"
ENROLLMENTS_CSV = DATA_DIR / "enrollment.csv"
TIMESLOTS_CSV = DATA_DIR / "timeslots.csv"
ROOMS_CSV = DATA_DIR / "rooms.csv"
SLOT_BLOCKS_CSV = DATA_DIR / "slot_blocks.csv"

# Faculty to Department Mapping (IPB Style)
FACULTY_DEPARTMENTS = {
    "FMIPA": ["ILKOM", "STAT", "MAT", "KIM", "FIS"],
    "FATETA": ["TIN", "TEP", "ITP", "SIL"],
    "FEM": ["MAN", "EKO", "AKT", "ESL"],
    "FEMA": ["GIZ", "KPM", "IKK"],
    "FAPET": ["INTP", "IPB"],
}

# General course markers
GENERAL_FACULTY = "GENERAL"
GENERAL_DEPARTMENT = "GENERAL"

# Constraint weights
WEIGHT_HARD_CONSTRAINT = 1000.0
WEIGHT_CONSECUTIVE_EXAMS = 10.0
WEIGHT_TOO_MANY_EXAMS = 5.0
WEIGHT_SPREAD_PENALTY = 30.0
WEIGHT_SAME_SEMESTER_SEPARATION = 3.0
WEIGHT_HIGH_ENROLLMENT_SEPARATION = 2.0
WEIGHT_PREFERRED_GAP = 1.0
WEIGHT_FRIDAY_AFTERNOON_PENALTY = 5.0
WEIGHT_MAX_EXAMS_PER_DAY = 200.0
WEIGHT_ROOM_CAPACITY = 300.0
WEIGHT_SLOT_BLOCK = 250.0

# Threshold for defining large/high enrollment courses
HIGH_ENROLLMENT_THRESHOLD = 300
