import csv
import random
from collections import Counter

from src.utils.constants import (
    COURSES_CSV,
    ENROLLMENTS_CSV,
    FACULTY_DEPARTMENTS,
    GENERAL_DEPARTMENT,
    GENERAL_FACULTY,
    STUDENTS_CSV,
    TIMESLOTS_CSV,
    ROOMS_CSV,
    SLOT_BLOCKS_CSV,
)


def generate_dataset() -> None:
    """Generate a highly constrained realistic dataset for testing exam timetabling.

    This dataset simulates a university (IPB University style) with:
    - 5 Faculties, each containing 2 Departments (total 10 departments).
    - 8 semesters of students, with ~130 students per department (total ~1300).
    - A multi-layered course structure (General, Faculty, Department, Electives).
    - Extremely high-density conflicts: Students take 6-7 courses per semester.
    - Exactly 10 available exam timeslots (5 days, 2 sessions per day).
    """
    random.seed(42)  # For reproducibility

    # Ensure data directory exists
    COURSES_CSV.parent.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------------------
    # 1. Generate Timeslots (5 days, 2 sessions per day = 10 timeslots)
    # ---------------------------------------------------------------------------
    timeslots = []
    slot_id = 1
    for day in range(1, 6):  # 5 days
        for session in range(1, 3):  # 2 sessions per day
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
        ("GEN201", "Metode Ilmiah", 6),
        ("GEN202", "Pendidikan Kewarganegaraan", 7),
        ("GEN203", "Etika Profesi", 8),
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
        "FMIPA": [("FMA101", "Kalkulus I", 1), ("FMA102", "Aljabar Linear", 2)],
        "FATETA": [("FTA101", "Fisika Dasar I", 1), ("FTA102", "Kimia Dasar", 2)],
        "FEM": [("FEM101", "Pengantar Ekonomi", 1), ("FEM102", "Pengantar Bisnis", 2)],
        "FEMA": [("FMA201", "Sosiologi Umum", 1), ("FMA202", "Ekologi Manusia", 2)],
        "FAPET": [("FPT101", "Biologi Umum", 1), ("FPT102", "Pengantar Peternakan", 2)],
    }
    for fac, list_cores in faculty_cores.items():
        for cid, name, sem in list_cores:
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

    # 2.3 Department Core Courses (4 per semester for semesters 2, 4, 6)
    dept_course_templates = {
        "ILKOM": [
            ("KOM201", "Pemrograman Dasar", 2),
            ("KOM202", "PBO", 2),
            ("KOM203", "Matematika Diskrit", 2),
            ("KOM204", "Arsitektur Komputer", 2),
            ("KOM401", "Struktur Data", 4),
            ("KOM402", "Sistem Operasi", 4),
            ("KOM403", "Analisis Algoritma", 4),
            ("KOM404", "Basis Data", 4),
            ("KOM601", "Jaringan Komputer", 6),
            ("KOM602", "Rekayasa Perangkat Lunak", 6),
            ("KOM603", "Kecerdasan Buatan", 6),
            ("KOM604", "Grafika Komputer", 6),
        ],
        "STAT": [
            ("STT201", "Metode Statistika I", 2),
            ("STT202", "Statistika Deskriptif", 2),
            ("STT203", "Matematika Statistika", 2),
            ("STT204", "Metode Pengambilan Sampel", 2),
            ("STT401", "Statistika Matematika I", 4),
            ("STT402", "Komputasi Statistika", 4),
            ("STT403", "Analisis Data Kategori", 4),
            ("STT404", "Rancangan Percobaan I", 4),
            ("STT601", "Analisis Regresi", 6),
            ("STT602", "Analisis Deret Waktu", 6),
            ("STT603", "Statistika Nonparametrik", 6),
            ("STT604", "Multivariat Statistika", 6),
        ],
        "TIN": [
            ("TIN201", "Pengantar Industri Pertanian", 2),
            ("TIN202", "Kimia Organik Industri", 2),
            ("TIN203", "Mikrobiologi Industri", 2),
            ("TIN204", "Satuan Operasi I", 2),
            ("TIN401", "Analisis Sistem Industri", 4),
            ("TIN402", "Ekonomi Teknik", 4),
            ("TIN403", "Teknik Tata Cara Kerja", 4),
            ("TIN404", "Perancangan Produk", 4),
            ("TIN601", "Pengendalian Mutu", 6),
            ("TIN602", "Tata Letak Pabrik", 6),
            ("TIN603", "Pemasaran Industri", 6),
            ("TIN604", "Manajemen Strategik", 6),
        ],
        "TEP": [
            ("TEP201", "Teknik Biosistem", 2),
            ("TEP202", "Menggambar Teknik", 2),
            ("TEP203", "Mekanika Teknik", 2),
            ("TEP204", "Dasar Biosistem", 2),
            ("TEP401", "Termodinamika", 4),
            ("TEP402", "Mekanika Fluida", 4),
            ("TEP403", "Kelistrikan Pertanian", 4),
            ("TEP404", "Energi dan Mesin Pertanian", 4),
            ("TEP601", "Alat Mesin Pertanian", 6),
            ("TEP602", "Teknik Pascapanen", 6),
            ("TEP603", "Instrumentasi Pengendalian", 6),
            ("TEP604", "Sistem Informasi Geografi", 6),
        ],
        "MAN": [
            ("MAN201", "Pengantar Manajemen", 2),
            ("MAN202", "Perilaku Organisasi", 2),
            ("MAN203", "Ekonomi Mikro Manajerial", 2),
            ("MAN204", "Akuntansi Manajemen", 2),
            ("MAN401", "Manajemen Keuangan", 4),
            ("MAN402", "Manajemen Pemasaran", 4),
            ("MAN403", "Manajemen Operasi", 4),
            ("MAN404", "Riset Pemasaran", 4),
            ("MAN601", "Manajemen Strategik", 6),
            ("MAN602", "Kewirausahaan", 6),
            ("MAN603", "Manajemen SDM", 6),
            ("MAN604", "Bisnis Internasional", 6),
        ],
        "EKO": [
            ("EKO201", "Mikroekonomi I", 2),
            ("EKO202", "Matematika Ekonomi", 2),
            ("EKO203", "Statistika Ekonomi", 2),
            ("EKO204", "Akuntansi Dasar", 2),
            ("EKO401", "Makroekonomi I", 4),
            ("EKO402", "Ekonometrika I", 4),
            ("EKO403", "Ekonomi Moneter I", 4),
            ("EKO404", "Ekonomi Publik I", 4),
            ("EKO601", "Ekonomi Pembangunan", 6),
            ("EKO602", "Sejarah Pemikiran Ekonomi", 6),
            ("EKO603", "Ekonomi Internasional", 6),
            ("EKO604", "Ekonomi Regional", 6),
        ],
        "GIZ": [
            ("GIZ201", "Dasar Nutrisi", 2),
            ("GIZ202", "Kimia Gizi", 2),
            ("GIZ203", "Anatomi Fisiologi", 2),
            ("GIZ204", "Sosio-Antropologi Gizi", 2),
            ("GIZ401", "Dietetika", 4),
            ("GIZ402", "Gizi Daur Kehidupan", 4),
            ("GIZ403", "Penilaian Status Gizi", 4),
            ("GIZ404", "Kemanan Pangan", 4),
            ("GIZ601", "Gizi Masyarakat", 6),
            ("GIZ602", "Konseling Gizi", 6),
            ("GIZ603", "Gizi Olahraga", 6),
            ("GIZ604", "Epidemiologi Gizi", 6),
        ],
        "KPM": [
            ("KPM201", "Pengantar Sosiologi", 2),
            ("KPM202", "Antropologi Sosial", 2),
            ("KPM203", "Ekologi Politik", 2),
            ("KPM204", "Dasar Komunikasi", 2),
            ("KPM401", "Penyuluhan Pembangunan", 4),
            ("KPM402", "Sosiologi Pedesaan", 4),
            ("KPM403", "Metode Penelitian Sosial", 4),
            ("KPM404", "Gender dan Pembangunan", 4),
            ("KPM601", "Komunikasi Politik", 6),
            ("KPM602", "Pengembangan Kelembagaan", 6),
            ("KPM603", "Resolusi Konflik", 6),
            ("KPM604", "Corporate Social Responsibility", 6),
        ],
        "INTP": [
            ("INTP201", "Anatomi Ternak", 2),
            ("INTP202", "Dasar Fisiologi Ternak", 2),
            ("INTP203", "Dasar Genetika Ternak", 2),
            ("INTP204", "Pengantar Ilmu Pakan", 2),
            ("INTP401", "Nutrisi Ternak", 4),
            ("INTP402", "Bahan Pakan Ternak", 4),
            ("INTP403", "Tatalaksana Padang Penggembalaan", 4),
            ("INTP404", "Manajemen Ternak Potong", 4),
            ("INTP601", "Fisiologi Reproduksi", 6),
            ("INTP602", "Pemuliaan Ternak", 6),
            ("INTP603", "Teknologi Pakan", 6),
            ("INTP604", "Tatalaksana Ternak Perah", 6),
        ],
        "IPB": [
            ("IPB201", "Dasar Agronomi", 2),
            ("IPB202", "Dasar Genetika Tumbuhan", 2),
            ("IPB203", "Dasar Hortikultura", 2),
            ("IPB204", "Kesuburan Tanah", 2),
            ("IPB401", "Fisiologi Tumbuhan", 4),
            ("IPB402", "Agroklimatologi", 4),
            ("IPB403", "Ilmu Gulma", 4),
            ("IPB404", "Teknologi Benih I", 4),
            ("IPB601", "Perlindungan Tanaman", 6),
            ("IPB602", "Pemuliaan Tanaman", 6),
            ("IPB603", "Bioteknologi Tanaman", 6),
            ("IPB604", "Pertanian Berkelanjutan", 6),
        ],
    }

    for dept, c_list in dept_course_templates.items():
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
        ("KOM702", "Cloud Computing", "FMIPA", "ILKOM"),
        ("STT701", "Big Data Analytics", "FMIPA", "STAT"),
        ("STT702", "Machine Learning", "FMIPA", "STAT"),
        ("TIN701", "Logistik Rantai Pasok", "FATETA", "TIN"),
        ("TEP701", "Energi Terbarukan", "FATETA", "TEP"),
        ("MAN701", "Perilaku Konsumen", "FEM", "MAN"),
        ("EKO701", "Ekonometrika Terapan", "FEM", "EKO"),
        ("GIZ701", "Pangan Fungsional", "FEMA", "GIZ"),
        ("KPM701", "Pengembangan Masyarakat", "FEMA", "KPM"),
        ("INTP701", "Industri Pakan", "FAPET", "INTP"),
        ("IPB701", "Pemuliaan Tanaman Lanjut", "FAPET", "IPB"),
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
            if (sem, fac) not in courses_by_sem_and_fac:
                courses_by_sem_and_fac[(sem, fac)] = []
            courses_by_sem_and_fac[(sem, fac)].append(cid)
        elif ctype == "DEPARTMENT":
            if (sem, dept) not in courses_by_sem_and_dept:
                courses_by_sem_and_dept[(sem, dept)] = []
            courses_by_sem_and_dept[(sem, dept)].append(cid)

    elective_ids_by_dept = {}
    for c in courses:
        if c["course_type"] == "ELECTIVE":
            d = c["department_id"]
            if d not in elective_ids_by_dept:
                elective_ids_by_dept[d] = []
            elective_ids_by_dept[d].append(c["course_id"])

    for fac, depts in FACULTY_DEPARTMENTS.items():
        for dept in depts:
            # Generate ~16 students per semester, total ~130 per department, total ~1300 overall
            for sem in range(1, 9):
                num_students_in_sem = 16 if sem != 8 else 18
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

                    # 1. General course of the semester (taken by ALL students in that sem)
                    if sem in general_courses_by_sem:
                        enrollments.append(
                            {
                                "student_id": sid,
                                "course_id": general_courses_by_sem[sem],
                            }
                        )

                    # 2. Faculty core courses (taken by semesters 1 and 2)
                    if sem in [1, 2] and (sem, fac) in courses_by_sem_and_fac:
                        for fcid in courses_by_sem_and_fac[(sem, fac)]:
                            enrollments.append({"student_id": sid, "course_id": fcid})

                    # 3. Department core courses (taken by semesters 2, 4, 6)
                    dept_sem = sem if sem in [2, 4, 6] else None
                    if dept_sem and (dept_sem, dept) in courses_by_sem_and_dept:
                        for cid in courses_by_sem_and_dept[(dept_sem, dept)]:
                            enrollments.append({"student_id": sid, "course_id": cid})

                    # 4. Elective courses (taken by senior semesters 5-8)
                    if sem in [5, 6, 7, 8] and dept in elective_ids_by_dept:
                        for ecid in elective_ids_by_dept[dept]:
                            enrollments.append({"student_id": sid, "course_id": ecid})

                    # 5. Repeating Students (60% chance for semesters 3, 5, 7) - High conflict density
                    if sem in [3, 5, 7] and random.random() < 0.6:
                        lower_sem = sem - 1
                        if (lower_sem, dept) in courses_by_sem_and_dept:
                            repeats = random.sample(
                                courses_by_sem_and_dept[(lower_sem, dept)], k=2
                            )
                            for rcid in repeats:
                                enrollments.append(
                                    {"student_id": sid, "course_id": rcid}
                                )

                    # 6. Cross-Department Enrollments (60% chance) - Interdependent global graph
                    if dept == "ILKOM" and sem == 4 and random.random() < 0.6:
                        enrollments.append({"student_id": sid, "course_id": "STT201"})
                    elif dept == "STAT" and sem == 4 and random.random() < 0.6:
                        enrollments.append({"student_id": sid, "course_id": "KOM401"})

    # ---------------------------------------------------------------------------
    # 4. Count Course Enrollments and Allocate Rooms
    # ---------------------------------------------------------------------------
    course_enrollment_counts = Counter(e["course_id"] for e in enrollments)

    # Fixed rooms as requested by user
    # 2 Large (300), 3 Medium (150), 5 Small (80)
    rooms = [
        {"room_id": "R001", "capacity": 300},
        {"room_id": "R002", "capacity": 300},
        {"room_id": "R003", "capacity": 150},
        {"room_id": "R004", "capacity": 150},
        {"room_id": "R005", "capacity": 150},
        {"room_id": "R006", "capacity": 80},
        {"room_id": "R007", "capacity": 80},
        {"room_id": "R008", "capacity": 80},
        {"room_id": "R009", "capacity": 80},
        {"room_id": "R010", "capacity": 80},
    ]

    with open(ROOMS_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["room_id", "capacity"])
        writer.writeheader()
        writer.writerows(rooms)

    # Assign room to each course based on enrollment
    # Alternate assignments for load balancing
    large_index = 0
    medium_index = 0
    small_index = 0

    large_rooms = ["R001", "R002"]
    medium_rooms = ["R003", "R004", "R005"]
    small_rooms = ["R006", "R007", "R008", "R009", "R010"]

    for course in courses:
        cid = course["course_id"]
        enrollment_count = course_enrollment_counts.get(cid, 0)
        
        if enrollment_count > 150:
            course["room_id"] = large_rooms[large_index % len(large_rooms)]
            large_index += 1
        elif enrollment_count > 80:
            course["room_id"] = medium_rooms[medium_index % len(medium_rooms)]
            medium_index += 1
        else:
            course["room_id"] = small_rooms[small_index % len(small_rooms)]
            small_index += 1

    # Write courses CSV
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
                "room_id",
            ],
        )
        writer.writeheader()
        writer.writerows(courses)

    # ---------------------------------------------------------------------------
    # 5. Generate Slot Blocks
    # ---------------------------------------------------------------------------
    # Prohibit FMIPA, FATETA, and FEM from scheduling during key timeslots
    # (e.g., Friday Afternoon and major blocks on Day 1/2) to squeeze Greedy algorithm
    slot_blocks = [
        {"faculty_id": "FMIPA", "day": 1, "session": 1},
        {"faculty_id": "FMIPA", "day": 1, "session": 2},
        {"faculty_id": "FATETA", "day": 2, "session": 1},
        {"faculty_id": "FATETA", "day": 2, "session": 2},
        {"faculty_id": "FEM", "day": 3, "session": 1},
        {"faculty_id": "FEM", "day": 3, "session": 2},
    ]

    with open(SLOT_BLOCKS_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["faculty_id", "day", "session"])
        writer.writeheader()
        writer.writerows(slot_blocks)

    # ---------------------------------------------------------------------------
    # 6. Write Students and Enrollments CSVs
    # ---------------------------------------------------------------------------
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

    print("Generated dataset:")
    print(f"- {len(timeslots)} timeslots saved to {TIMESLOTS_CSV}")
    print(f"- {len(courses)} courses saved to {COURSES_CSV}")
    print(f"- {len(students)} students saved to {STUDENTS_CSV}")
    print(f"- {len(enrollments)} enrollments saved to {ENROLLMENTS_CSV}")
