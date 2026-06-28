import csv
import random

from src.utils.constants import (
    COURSES_CSV,
    ENROLLMENTS_CSV,
    FACULTY_DEPARTMENTS,
    GENERAL_DEPARTMENT,
    GENERAL_FACULTY,
    STUDENTS_CSV,
    TIMESLOTS_CSV,
)


def generate_dataset() -> None:
    """Generate a highly constrained realistic dataset for testing exam timetabling.

    This dataset simulates a university (IPB University style) with:
    - 5 Faculties, each containing 2 Departments (total 10 departments).
    - 8 semesters of students, with ~130 students per department (total ~1300).
    - A multi-layered course structure (General, Faculty, Department, Electives).
    - Repeating students (students in odd semesters retaking lower courses).
    - Cross-department enrollments (e.g., Computer Science taking Statistics).
    - Choice of electives by senior students.
    - 15 available exam timeslots (5 days, 3 sessions per day).
    """
    random.seed(42)  # For reproducibility

    # Ensure data directory exists
    COURSES_CSV.parent.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------------------
    # 1. Generate Timeslots
    # ---------------------------------------------------------------------------
    timeslots = []
    slot_id = 1
    for day in range(1, 6):  # 5 days
        for session in range(1, 4):  # 3 sessions per day
            timeslots.append({"slot_id": slot_id, "day": day, "session": session})
            slot_id += 1

    with open(TIMESLOTS_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["slot_id", "day", "session"])
        writer.writeheader()
        writer.writerows(timeslots)

    # ---------------------------------------------------------------------------
    # 2. Generate Courses
    # ---------------------------------------------------------------------------
    courses = []

    # 2.1 General University Courses (High enrollment, taken across all departments)
    general_courses = [
        ("GEN101", "Pancasila", 1),
        ("GEN102", "Pendidikan Agama", 2),
        ("GEN103", "Bahasa Indonesia", 3),
        ("GEN104", "Bahasa Inggris", 4),
        ("GEN105", "Kewirausahaan", 5),
    ]
    for cid, name, sem in general_courses:
        courses.append(
            {
                "course_id": cid,
                "course_name": name,
                "faculty_id": GENERAL_FACULTY,
                "department_id": GENERAL_DEPARTMENT,
                "offered_semester": sem,
                "course_type": "GENERAL",
            }
        )

    # 2.2 Faculty Core Courses (Taken by all students within a faculty)
    faculty_cores = {
        "FMIPA": ("FMA101", "Kalkulus", 1),
        "FATETA": ("FTA101", "Fisika Dasar", 1),
        "FEM": ("FEM101", "Pengantar Ekonomi", 1),
        "FEMA": ("FMA102", "Sosiologi Umum", 1),
        "FAPET": ("FPT101", "Biologi Umum", 1),
    }
    for fac, (cid, name, sem) in faculty_cores.items():
        courses.append(
            {
                "course_id": cid,
                "course_name": name,
                "faculty_id": fac,
                "department_id": GENERAL_DEPARTMENT,
                "offered_semester": sem,
                "course_type": "FACULTY",
            }
        )

    # 2.3 Department Core Courses (Offered in semester 2, 4, and 6)
    dept_course_templates = {
        "ILKOM": [
            ("KOM201", "Pemrograman Dasar", 2),
            ("KOM401", "Struktur Data", 4),
            ("KOM601", "Basis Data", 6),
        ],
        "STAT": [
            ("STT201", "Metode Statistika I", 2),
            ("STT401", "Statistika Matematika I", 4),
            ("STT601", "Analisis Regresi", 6),
        ],
        "TIN": [
            ("TIN201", "Pengantar Industri Pertanian", 2),
            ("TIN401", "Analisis Sistem Industri", 4),
            ("TIN601", "Pengendalian Mutu", 6),
        ],
        "TEP": [
            ("TEP201", "Teknik Biosistem", 2),
            ("TEP401", "Termodinamika", 4),
            ("TEP601", "Alat Mesin Pertanian", 6),
        ],
        "MAN": [
            ("MAN201", "Pengantar Manajemen", 2),
            ("MAN401", "Manajemen Keuangan", 4),
            ("MAN601", "Manajemen Strategik", 6),
        ],
        "EKO": [
            ("EKO201", "Mikroekonomi I", 2),
            ("EKO401", "Makroekonomi I", 4),
            ("EKO601", "Ekonomi Pembangunan", 6),
        ],
        "GIZ": [
            ("GIZ201", "Dasar Nutrisi", 2),
            ("GIZ401", "Dietetika", 4),
            ("GIZ601", "Gizi Masyarakat", 6),
        ],
        "KPM": [
            ("KPM201", "Pengantar Sosiologi", 2),
            ("KPM401", "Penyuluhan Pembangunan", 4),
            ("KPM601", "Komunikasi Politik", 6),
        ],
        "INTP": [
            ("INTP201", "Anatomi Ternak", 2),
            ("INTP401", "Nutrisi Ternak", 4),
            ("INTP601", "Fisiologi Reproduksi", 6),
        ],
        "IPB": [
            ("IPB201", "Dasar Agronomi", 2),
            ("IPB401", "Fisiologi Tumbuhan", 4),
            ("IPB601", "Perlindungan Tanaman", 6),
        ],
    }

    for dept, c_list in dept_course_templates.items():
        # Find which faculty this department belongs to
        fac_id = next(
            fac for fac, depts in FACULTY_DEPARTMENTS.items() if dept in depts
        )
        for cid, name, sem in c_list:
            courses.append(
                {
                    "course_id": cid,
                    "course_name": name,
                    "faculty_id": fac_id,
                    "department_id": dept,
                    "offered_semester": sem,
                    "course_type": "DEPARTMENT",
                }
            )

    # 2.4 Elective Courses (Offered in semester 7, taken by senior students)
    electives = [
        ("KOM701", "Deep Learning", "FMIPA", "ILKOM"),
        ("STT701", "Big Data Analytics", "FMIPA", "STAT"),
        ("TIN701", "Logistik Rantai Pasok", "FATETA", "TIN"),
        ("TEP701", "Energi Terbarukan", "FATETA", "TEP"),
        ("MAN701", "Perilaku Konsumen", "FEM", "MAN"),
        ("EKO701", "Ekonometrika", "FEM", "EKO"),
        ("GIZ701", "Pangan Fungsional", "FEMA", "GIZ"),
        ("KPM701", "Pengembangan Masyarakat", "FEMA", "KPM"),
        ("INTP701", "Industri Pakan", "FAPET", "INTP"),
        ("IPB701", "Pemuliaan Tanaman", "FAPET", "IPB"),
    ]
    for cid, name, fac, dept in electives:
        courses.append(
            {
                "course_id": cid,
                "course_name": name,
                "faculty_id": fac,
                "department_id": dept,
                "offered_semester": 7,
                "course_type": "ELECTIVE",
            }
        )

    with open(COURSES_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "course_id",
                "course_name",
                "faculty_id",
                "department_id",
                "offered_semester",
                "course_type",
            ],
        )
        writer.writeheader()
        writer.writerows(courses)

    # ---------------------------------------------------------------------------
    # 3. Generate Students & Enrollments
    # ---------------------------------------------------------------------------
    students = []
    enrollments = []
    student_counter = 1

    # Map courses for quick lookup by category
    courses_by_sem_and_dept = {}
    courses_by_sem_and_fac = {}
    general_courses_by_sem = {}

    for c in courses:
        cid = c["course_id"]
        sem = c["offered_semester"]
        ctype = c["course_type"]
        dept = c["department_id"]
        fac = c["faculty_id"]

        if ctype == "GENERAL":
            general_courses_by_sem[sem] = cid
        elif ctype == "FACULTY":
            courses_by_sem_and_fac[(sem, fac)] = cid
        elif ctype == "DEPARTMENT":
            courses_by_sem_and_dept[(sem, dept)] = cid

    elective_ids = [c["course_id"] for c in courses if c["course_type"] == "ELECTIVE"]

    for fac, depts in FACULTY_DEPARTMENTS.items():
        for dept in depts:
            # 130 students per department, distributed evenly over 8 semesters
            # Semester 1-8. Let's create ~16 students per semester.
            for sem in range(1, 9):
                num_students_in_sem = 16 if sem != 8 else 18  # 16 * 7 + 18 = 130
                for _ in range(num_students_in_sem):
                    sid = f"S{student_counter:04d}"
                    student_counter += 1

                    students.append(
                        {
                            "student_id": sid,
                            "faculty_id": fac,
                            "department_id": dept,
                            "current_semester": sem,
                        }
                    )

                    # Enroll in general courses for this semester (if applicable)
                    if sem in general_courses_by_sem:
                        enrollments.append(
                            {
                                "student_id": sid,
                                "course_id": general_courses_by_sem[sem],
                            }
                        )

                    # Enroll in faculty core course for semester 1
                    if sem == 1 and (1, fac) in courses_by_sem_and_fac:
                        enrollments.append(
                            {
                                "student_id": sid,
                                "course_id": courses_by_sem_and_fac[(1, fac)],
                            }
                        )

                    # Enroll in department core course for the student's semester
                    # (e.g. sem 2, 4, 6)
                    # To be realistic, students take their current semester's core.
                    dept_sem = sem if sem in [2, 4, 6] else None
                    if dept_sem and (dept_sem, dept) in courses_by_sem_and_dept:
                        enrollments.append(
                            {
                                "student_id": sid,
                                "course_id": courses_by_sem_and_dept[(dept_sem, dept)],
                            }
                        )

                    # Simulate Repeating Students (15% chance for semesters 3, 5, 7)
                    if sem in [3, 5, 7] and random.random() < 0.15:
                        lower_sem = sem - 1
                        if (lower_sem, dept) in courses_by_sem_and_dept:
                            enrollments.append(
                                {
                                    "student_id": sid,
                                    "course_id": courses_by_sem_and_dept[
                                        (lower_sem, dept)
                                    ],
                                }
                            )

                    # Simulate Cross-Department Enrollments (10% chance)
                    # E.g. ILKOM students in sem 4 take STAT methods;
                    # STAT students take ILKOM Data Structures (KOM401).
                    if dept == "ILKOM" and sem == 4 and random.random() < 0.10:
                        # Enroll in STAT Metode Statistika I (STT201)
                        enrollments.append({"student_id": sid, "course_id": "STT201"})
                    elif dept == "STAT" and sem == 4 and random.random() < 0.10:
                        # Enroll in ILKOM Struktur Data (KOM401)
                        enrollments.append({"student_id": sid, "course_id": "KOM401"})

                    # Simulate Electives for Senior Students (Semesters 5-8)
                    if sem in [5, 6, 7, 8]:
                        # Pick 1 random elective from the global elective list
                        chosen_elective = random.choice(elective_ids)
                        enrollments.append(
                            {"student_id": sid, "course_id": chosen_elective}
                        )

    with open(STUDENTS_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "student_id",
                "faculty_id",
                "department_id",
                "current_semester",
            ],
        )
        writer.writeheader()
        writer.writerows(students)

    with open(ENROLLMENTS_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "course_id"])
        writer.writeheader()
        writer.writerows(enrollments)

    print(
        f"Generated dataset:\n"
        f"- {len(timeslots)} timeslots saved to {TIMESLOTS_CSV}\n"
        f"- {len(courses)} courses saved to {COURSES_CSV}\n"
        f"- {len(students)} students saved to {STUDENTS_CSV}\n"
        f"- {len(enrollments)} enrollments saved to {ENROLLMENTS_CSV}"
    )


if __name__ == "__main__":
    generate_dataset()
