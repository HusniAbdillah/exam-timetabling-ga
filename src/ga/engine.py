import logging
import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field

from src.ga.chromosome import (
    Chromosome,
    ConflictMatrix,
    FitnessHistory,
    Population,
)
from src.ga.crossover import one_point_crossover, uniform_crossover
from src.ga.elitism import apply_elitism
from src.ga.mutation import move_mutation, swap_mutation
from src.ga.population import initialize_population
from src.ga.selection import tournament_selection

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Type alias for the fitness callable
# ---------------------------------------------------------------------------

FitnessFn = Callable[[Chromosome, ConflictMatrix, list[int]], float]
"""Signature expected of any fitness function passed to ``run_ga``.

Args:
    chromosome: The candidate solution to evaluate.
    conflict_matrix: Adjacency list of course conflicts.
    timeslots: Ordered list of available timeslot IDs.

Returns:
    A non-negative penalty value. Lower values indicate better solutions.
"""


# ---------------------------------------------------------------------------
# Configuration dataclass
# ---------------------------------------------------------------------------


@dataclass
class GAConfig:
    """Hyperparameters for the Genetic Algorithm.

    Attributes:
        population_size: Number of individuals per generation.
        max_generations: Number of evolutionary iterations to run.
        crossover_rate: Probability that two selected parents undergo crossover.
            When crossover does not occur, the parents are copied directly.
        mutation_rate: Probability controlling how aggressively offspring are
            mutated (interpretation varies by operator).
        tournament_size: Number of candidates drawn for each tournament
            selection event.
        elite_count: Number of best individuals preserved unchanged into the
            next generation (elitism).
    """

    population_size: int = 100
    max_generations: int = 200
    crossover_rate: float = 0.8
    mutation_rate: float = 0.1
    tournament_size: int = 5
    elite_count: int = 2
    enable_repair: bool = False


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class GAResult:
    """Output produced by the Genetic Algorithm engine.

    Attributes:
        best_solution: The chromosome with the lowest observed penalty.
        best_fitness: Penalty value of ``best_solution``.
        fitness_history: Best fitness recorded at the end of each generation.
            ``fitness_history[i]`` is the best fitness after generation ``i+1``.
        generation: Total number of generations executed.
        execution_time: Wall-clock seconds elapsed during ``run_ga``.
    """

    best_solution: Chromosome
    best_fitness: float
    fitness_history: FitnessHistory = field(default_factory=list)
    generation: int = 0
    execution_time: float = 0.0


# ---------------------------------------------------------------------------
# Main GA engine
# ---------------------------------------------------------------------------


def run_ga(
    courses: list[str],
    timeslots: list[int],
    conflict_matrix: ConflictMatrix,
    config: GAConfig,
    fitness_fn: FitnessFn,
    seeds: list[Chromosome] | None = None,
) -> GAResult:
    """Run the Genetic Algorithm to produce an optimized exam timetable.

    The algorithm follows a standard generational GA loop:

    1. Initialise a population (optionally seeded).
    2. Evaluate fitness for every individual.
    3. Preserve elite individuals unchanged.
    4. Fill the rest of the next generation by selecting parents via
       tournament selection, applying crossover, then mutation.
    5. Repeat until ``config.max_generations`` is reached.
    6. Return the best solution found across all generations.

    Crossover operator is chosen uniformly at random between
    :func:`one_point_crossover` and :func:`uniform_crossover`.

    Mutation operator is chosen uniformly at random between
    :func:`swap_mutation` and :func:`move_mutation`.

    Args:
        courses: Ordered list of course IDs.  The position of each course in
            this list determines its index in the chromosome.
        timeslots: Ordered list of available timeslot IDs (1-indexed integers).
        conflict_matrix: Adjacency list mapping each course ID to the set of
            course IDs it conflicts with.
        config: GA hyperparameters.
        fitness_fn: Callable that computes the penalty for a given chromosome.
            See :data:`FitnessFn` for the expected signature.
        seeds: Optional list of pre-configured chromosomes to seed the population.

    Returns:
        A :class:`GAResult` containing the best chromosome found, its fitness,
        the per-generation fitness history, and timing information.
    """
    num_courses = len(courses)
    num_timeslots = len(timeslots)

    logger.info(
        "Starting GA: courses=%d, timeslots=%d, population=%d, generations=%d",
        num_courses,
        num_timeslots,
        config.population_size,
        config.max_generations,
    )

    start_time = time.monotonic()

    population: Population = initialize_population(
        num_courses, num_timeslots, config.population_size, seeds
    )

    fitness_history: FitnessHistory = []
    best_solution: Chromosome = population[0][:]
    best_fitness: float = float("inf")

    for generation in range(1, config.max_generations + 1):
        # ------------------------------------------------------------------ #
        # Evaluate fitness
        # ------------------------------------------------------------------ #
        fitness_values: list[float] = [
            fitness_fn(chrom, conflict_matrix, timeslots) for chrom in population
        ]

        # Track global best across all generations
        gen_best_idx = min(range(len(population)), key=lambda i: fitness_values[i])
        gen_best_fitness = fitness_values[gen_best_idx]

        if gen_best_fitness < best_fitness:
            best_fitness = gen_best_fitness
            best_solution = population[gen_best_idx][:]

        fitness_history.append(best_fitness)

        logger.debug(
            "Generation %d/%d — best_fitness=%.2f",
            generation,
            config.max_generations,
            best_fitness,
        )

        # ------------------------------------------------------------------ #
        # Early stopping: perfect solution found
        # ------------------------------------------------------------------ #
        if best_fitness == 0.0:
            logger.info("Perfect solution found at generation %d.", generation)
            break

        # ------------------------------------------------------------------ #
        # Elitism
        # ------------------------------------------------------------------ #
        elites: Population = apply_elitism(
            population, fitness_values, config.elite_count
        )

        # ------------------------------------------------------------------ #
        # Build next generation
        # ------------------------------------------------------------------ #
        slots_for_offspring = config.population_size - len(elites)
        next_population: Population = []

        while len(next_population) < slots_for_offspring:
            parent1 = tournament_selection(
                population, fitness_values, config.tournament_size
            )
            parent2 = tournament_selection(
                population, fitness_values, config.tournament_size
            )

            # Crossover
            if random.random() < config.crossover_rate:
                if random.random() < 0.5:
                    child1, child2 = one_point_crossover(parent1, parent2)
                else:
                    child1, child2 = uniform_crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            # Mutation (operator chosen randomly each time)
            if random.random() < 0.5:
                child1 = swap_mutation(child1, config.mutation_rate)
                child2 = swap_mutation(child2, config.mutation_rate)
            else:
                child1 = move_mutation(child1, num_timeslots, config.mutation_rate)
                child2 = move_mutation(child2, num_timeslots, config.mutation_rate)

            # Apply greedy repair if enabled (Memetic GA local search probability = 0.2)
            if config.enable_repair and random.random() < 0.20:
                child1 = repair_chromosome(
                    child1, courses, conflict_matrix, timeslots, fitness_fn
                )
                child2 = repair_chromosome(
                    child2, courses, conflict_matrix, timeslots, fitness_fn
                )

            next_population.append(child1)
            if len(next_population) < slots_for_offspring:
                next_population.append(child2)

        population = elites + next_population

    execution_time = time.monotonic() - start_time

    logger.info(
        "GA complete: best_fitness=%.2f, generations=%d, time=%.3fs",
        best_fitness,
        generation,
        execution_time,
    )

    return GAResult(
        best_solution=best_solution,
        best_fitness=best_fitness,
        fitness_history=fitness_history,
        generation=generation,
        execution_time=execution_time,
    )


def repair_chromosome(
    chromosome: Chromosome,
    courses: list[str],
    conflict_matrix: ConflictMatrix,
    timeslots: list[int],
    fitness_fn: FitnessFn,
) -> Chromosome:
    """Greedy repair mechanism for Hybrid GA.

    It identifies courses that actively cause student exam clashes,
    and tries reassigning up to 3 of them to other timeslots to minimize penalty.
    """
    repaired = chromosome[:]
    # Find only courses that are actively conflicting in the current schedule
    conflicting_indices = []
    for i in range(len(repaired)):
        cid_i = courses[i]
        slot_i = repaired[i]
        for j in range(len(repaired)):
            if i != j and repaired[j] == slot_i:
                if courses[j] in conflict_matrix.get(cid_i, set()):
                    conflicting_indices.append(i)
                    break

    if not conflicting_indices:
        return repaired

    # Limit to maximum 3 conflicting courses to repair per invocation for high performance
    random.shuffle(conflicting_indices)
    num_to_repair = min(3, len(conflicting_indices))

    for idx in conflicting_indices[:num_to_repair]:
        current_slot = repaired[idx]
        current_penalty = fitness_fn(repaired, conflict_matrix, timeslots)

        if current_penalty == 0.0:
            break

        best_slot = current_slot
        best_penalty = current_penalty

        # Try other slots
        for slot in timeslots:
            if slot == current_slot:
                continue
            repaired[idx] = slot
            penalty = fitness_fn(repaired, conflict_matrix, timeslots)
            if penalty < best_penalty:
                best_penalty = penalty
                best_slot = slot

        repaired[idx] = best_slot
    return repaired
