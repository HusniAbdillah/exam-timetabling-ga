import random
from typing import TypeAlias

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

Chromosome: TypeAlias = list[int]
"""A single solution represented as a list of timeslot IDs.

Each index corresponds to a course (ordered as in courses.csv).
Each value is the timeslot ID assigned to that course.
"""

Population: TypeAlias = list[Chromosome]
"""A collection of chromosomes forming one generation."""

FitnessHistory: TypeAlias = list[float]
"""Sequence of best fitness values recorded each generation."""

ConflictMatrix: TypeAlias = dict[str, set[str]]
"""Adjacency list mapping a course ID to the set of course IDs it conflicts with.

Two courses conflict when at least one student is enrolled in both.
"""


# ---------------------------------------------------------------------------
# Chromosome factory
# ---------------------------------------------------------------------------


def create_random_chromosome(num_courses: int, num_timeslots: int) -> Chromosome:
    """Create a chromosome with a random timeslot assigned to each course.

    Args:
        num_courses: Total number of courses to schedule.
        num_timeslots: Number of available timeslot IDs (slots are 1-indexed).

    Returns:
        A chromosome of length ``num_courses`` with values in
        ``[1, num_timeslots]``.
    """
    return [random.randint(1, num_timeslots) for _ in range(num_courses)]
