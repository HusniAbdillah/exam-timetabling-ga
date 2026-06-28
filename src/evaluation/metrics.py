from src.fitness.fitness import evaluate_constraints
from src.ga.chromosome import Chromosome


def evaluate_schedule_metrics(chromosome: Chromosome) -> dict[str, float | int]:
    """Evaluate and return a dictionary of detailed metrics for a schedule.

    Args:
        chromosome: Candidate solution mapping course index to slot ID.

    Returns:
        dict: Detailed breakdown of constraint violations and penalties.
    """
    return evaluate_constraints(chromosome)
