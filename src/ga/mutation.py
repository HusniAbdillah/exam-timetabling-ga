import random

from src.ga.chromosome import Chromosome


def swap_mutation(
    chromosome: Chromosome,
    mutation_rate: float,
) -> Chromosome:
    """Apply swap mutation to a chromosome.

    With probability ``mutation_rate`` two random gene positions are chosen
    and their timeslot values are exchanged. This preserves the multiset of
    assigned timeslots, only altering which course maps to which slot.

    Args:
        chromosome: The chromosome to (potentially) mutate.
        mutation_rate: Probability that a swap occurs. Must be in ``[0.0, 1.0]``.

    Returns:
        A new chromosome. The original is never modified.
    """
    mutated = chromosome[:]

    if len(mutated) >= 2 and random.random() < mutation_rate:
        i, j = random.sample(range(len(mutated)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]

    return mutated


def move_mutation(
    chromosome: Chromosome,
    num_timeslots: int,
    mutation_rate: float,
) -> Chromosome:
    """Apply move mutation to a chromosome.

    For each gene, independently with probability ``mutation_rate``, the
    timeslot assigned to that course is replaced with a uniformly random
    timeslot drawn from ``[1, num_timeslots]``.

    This operator directly explores the timeslot reassignment space and is
    well-suited for escaping local optima caused by hard constraint violations.

    Args:
        chromosome: The chromosome to (potentially) mutate.
        num_timeslots: Total number of available timeslot IDs (1-indexed).
        mutation_rate: Per-gene probability of reassignment.
            Must be in ``[0.0, 1.0]``.

    Returns:
        A new chromosome. The original is never modified.
    """
    mutated = chromosome[:]

    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = random.randint(1, num_timeslots)

    return mutated
