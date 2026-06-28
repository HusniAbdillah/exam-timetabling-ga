import random

from src.ga.chromosome import Chromosome


def one_point_crossover(
    parent1: Chromosome,
    parent2: Chromosome,
) -> tuple[Chromosome, Chromosome]:
    """Produce two offspring via one-point crossover.

    A single cut-point is chosen uniformly at random in the range
    ``[1, len(parent1) - 1]``. Genes before the cut-point are inherited
    from the same parent; genes from the cut-point onward are swapped.

    Example::

        parent1 = [1, 2, 3 | 4, 5]
        parent2 = [6, 7, 8 | 9, 10]
        child1  = [1, 2, 3,  9, 10]
        child2  = [6, 7, 8,  4,  5]

    Args:
        parent1: First parent chromosome.
        parent2: Second parent chromosome. Must have the same length as
            ``parent1``.

    Returns:
        A tuple ``(child1, child2)`` produced by crossing over the two parents.
    """
    n = len(parent1)
    if n <= 1:
        return parent1[:], parent2[:]

    point = random.randint(1, n - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def uniform_crossover(
    parent1: Chromosome,
    parent2: Chromosome,
    swap_prob: float = 0.5,
) -> tuple[Chromosome, Chromosome]:
    """Produce two offspring via uniform crossover.

    For each gene position, the two children independently swap genes with
    probability ``swap_prob``. When a swap occurs, child 1 takes the gene
    from parent 2 and vice versa.

    Args:
        parent1: First parent chromosome.
        parent2: Second parent chromosome. Must have the same length as
            ``parent1``.
        swap_prob: Probability of swapping genes at each position.
            Defaults to 0.5 (equal chance of inheriting from either parent).

    Returns:
        A tuple ``(child1, child2)`` produced by uniformly mixing the parents.
    """
    child1: Chromosome = []
    child2: Chromosome = []

    for g1, g2 in zip(parent1, parent2, strict=True):
        if random.random() < swap_prob:
            child1.append(g2)
            child2.append(g1)
        else:
            child1.append(g1)
            child2.append(g2)

    return child1, child2
