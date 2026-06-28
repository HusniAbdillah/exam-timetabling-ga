from src.ga.chromosome import Chromosome, Population, create_random_chromosome


def initialize_population(
    num_courses: int,
    num_timeslots: int,
    population_size: int,
    seeds: list[Chromosome] | None = None,
) -> Population:
    """Create an initial population of chromosomes, optionally starting with seed individuals.

    Each chromosome is independently randomized, unless pre-seeded.

    Args:
        num_courses: Number of courses to schedule (chromosome length).
        num_timeslots: Number of available timeslot IDs (slots are 1-indexed).
        population_size: Number of individuals in the population.
        seeds: Optional list of pre-configured chromosomes to seed the population.

    Returns:
        A list of ``population_size`` chromosomes.
    """
    pop = []
    if seeds:
        for s in seeds:
            pop.append(s[:])
    while len(pop) < population_size:
        pop.append(create_random_chromosome(num_courses, num_timeslots))
    return pop


def get_population_stats(
    population: Population,
    fitness_values: list[float],
) -> dict[str, float]:
    """Compute basic statistics about the current population.

    Args:
        population: The current generation of chromosomes.
        fitness_values: Corresponding fitness (penalty) value for each individual.

    Returns:
        A dictionary with keys ``min``, ``max``, and ``mean`` fitness.
    """
    if not fitness_values:
        return {"min": 0.0, "max": 0.0, "mean": 0.0}

    return {
        "min": min(fitness_values),
        "max": max(fitness_values),
        "mean": sum(fitness_values) / len(fitness_values),
    }
