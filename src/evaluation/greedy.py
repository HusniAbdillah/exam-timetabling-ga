import time

from src.fitness.fitness import (
    calculate_fitness,
    initialize_fitness_data,
)
from src.ga.chromosome import Chromosome, ConflictMatrix
from src.ga.engine import GAResult
from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.student import Student
from src.models.timeslot import Timeslot


def run_greedy(
    students: list[Student],
    courses: list[Course],
    enrollments: list[Enrollment],
    timeslots: list[Timeslot],
    conflict_matrix: ConflictMatrix,
) -> GAResult:
    """Run a deterministic Greedy algorithm to schedule exams.

    Courses are sorted by their degree of conflict (number of conflicting courses).
    For each course, we evaluate all available timeslots and assign the one
    that minimizes the total penalty.

    Args:
        students: List of Student objects.
        courses: List of Course objects.
        enrollments: List of Enrollment objects.
        timeslots: List of Timeslot objects.
        conflict_matrix: Adjacency list of course conflicts.

    Returns:
        GAResult: Contain the best solution found, its fitness, and execution time.
    """
    start_time = time.monotonic()

    # Initialize fitness data for evaluation
    initialize_fitness_data(students, courses, enrollments, timeslots)

    num_courses = len(courses)
    slot_ids = [t.slot_id for t in timeslots]

    # Create mapping of course_id to index in the original courses list
    course_indices = {c.course_id: idx for idx, c in enumerate(courses)}

    # Sort courses by conflict degree (most conflicted first)
    sorted_courses = sorted(
        courses,
        key=lambda c: len(conflict_matrix.get(c.course_id, set())),
        reverse=True,
    )

    # Initialize chromosome with dummy slots (e.g., slot 1 for all)
    # We will build it incrementally.
    chromosome: Chromosome = [1] * num_courses

    # Keep track of already scheduled courses
    scheduled_indices: set[int] = set()

    for course in sorted_courses:
        c_idx = course_indices[course.course_id]
        best_slot = 1
        best_penalty = float("inf")

        # Test all timeslots for the current course
        for slot in slot_ids:
            chromosome[c_idx] = slot
            # Calculate fitness for the current partial chromosome
            # (only looking at scheduled courses and the current one)
            penalty = calculate_fitness(chromosome, conflict_matrix, slot_ids)

            if penalty < best_penalty:
                best_penalty = penalty
                best_slot = slot

        # Fix the best slot for this course
        chromosome[c_idx] = best_slot
        scheduled_indices.add(c_idx)

    execution_time = time.monotonic() - start_time
    final_fitness = calculate_fitness(chromosome, conflict_matrix, slot_ids)

    return GAResult(
        best_solution=chromosome,
        best_fitness=final_fitness,
        fitness_history=[final_fitness],
        generation=1,
        execution_time=execution_time,
    )
