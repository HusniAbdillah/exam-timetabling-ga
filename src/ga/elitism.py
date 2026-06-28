from src.ga.chromosome import Population


def apply_elitism(
    population: Population,
    fitness_values: list[float],
    elite_count: int,
) -> Population:
    """Preserve the best individuals across generations.

    Sorts the population by ascending fitness (lowest penalty first) and
    returns deep copies of the top ``elite_count`` chromosomes. These elites
    are re-inserted into the next generation unchanged, guaranteeing that the
    best solution found so far is never lost.

    Args:
        population: The current generation of chromosomes.
        fitness_values: Corresponding fitness (penalty) value for each individual.
            Must have the same length as ``population``.
        elite_count: Number of top individuals to preserve. If 0, an empty list
            is returned. Clamped to ``len(population)`` if larger.

    Returns:
        A list of ``elite_count`` chromosomes, ordered from best to worst.
        Each entry is an independent copy of the original chromosome.
    """
    if elite_count <= 0:
        return []

    effective_count = min(elite_count, len(population))
    sorted_indices = sorted(range(len(population)), key=lambda i: fitness_values[i])
    return [population[i][:] for i in sorted_indices[:effective_count]]
