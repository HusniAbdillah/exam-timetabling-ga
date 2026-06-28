import random

from src.ga.chromosome import Chromosome, Population


def tournament_selection(
    population: Population,
    fitness_values: list[float],
    tournament_size: int,
) -> Chromosome:
    """Select an individual from the population using tournament selection.

    A random subset of ``tournament_size`` individuals is sampled from the
    population (without replacement). The individual with the lowest fitness
    value (lowest penalty) wins the tournament and is returned.

    Args:
        population: The current generation of chromosomes.
        fitness_values: Corresponding fitness (penalty) value for each individual.
            Lower values indicate better solutions.
        tournament_size: Number of individuals that compete in each tournament.
            Must be >= 1 and <= len(population).

    Returns:
        A copy of the winning chromosome.

    Raises:
        ValueError: If ``tournament_size`` is less than 1 or greater than the
            population size.
    """
    if tournament_size < 1:
        raise ValueError(f"tournament_size must be at least 1, got {tournament_size}")
    if tournament_size > len(population):
        raise ValueError(
            f"tournament_size ({tournament_size}) exceeds population size "
            f"({len(population)})"
        )

    candidate_indices = random.sample(range(len(population)), tournament_size)
    winner_index = min(candidate_indices, key=lambda i: fitness_values[i])
    return population[winner_index][:]
