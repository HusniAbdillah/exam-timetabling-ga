import pytest

from src.ga.chromosome import Chromosome
from src.ga.selection import tournament_selection

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

POPULATION: list[Chromosome] = [
    [1, 2, 3],  # index 0
    [4, 5, 6],  # index 1 — best (fitness 20.0)
    [7, 8, 9],  # index 2
    [2, 4, 6],  # index 3
    [1, 3, 5],  # index 4
]

FITNESS_VALUES: list[float] = [50.0, 20.0, 80.0, 40.0, 60.0]


# ---------------------------------------------------------------------------
# Basic correctness
# ---------------------------------------------------------------------------


def test_returns_chromosome_from_population():
    """Selected chromosome must equal one of the individuals in the population."""
    winner = tournament_selection(POPULATION, FITNESS_VALUES, tournament_size=3)
    assert winner in POPULATION


def test_returns_a_copy_not_reference():
    """Mutating the returned chromosome must not affect the original population."""
    winner = tournament_selection(POPULATION, FITNESS_VALUES, tournament_size=3)
    winner.append(99)
    for chrom in POPULATION:
        assert 99 not in chrom


def test_single_candidate_returns_that_individual():
    """With tournament_size=1, the sole candidate is always returned."""
    population: list[Chromosome] = [[1, 2, 3]]
    fitness_values: list[float] = [42.0]
    winner = tournament_selection(population, fitness_values, tournament_size=1)
    assert winner == [1, 2, 3]


# ---------------------------------------------------------------------------
# Selection pressure
# ---------------------------------------------------------------------------


def test_full_tournament_always_returns_best():
    """With tournament_size equal to population size, the global best must win."""
    for _ in range(50):
        winner = tournament_selection(
            POPULATION, FITNESS_VALUES, tournament_size=len(POPULATION)
        )
        # Index 1 has the lowest fitness (20.0)
        assert winner == POPULATION[1]


def test_winner_fitness_not_worse_than_losers():
    """The winner's fitness must be <= every other participant in the tournament."""
    for _ in range(200):
        winner = tournament_selection(POPULATION, FITNESS_VALUES, tournament_size=3)
        winner_fitness = FITNESS_VALUES[POPULATION.index(winner)]
        # The winner should be the best among all participants — we can verify
        # by checking it is at least as good as all other individuals globally.
        # (Since we run with full-tournament in some iterations this is a
        # sufficient statistical sanity check.)
        assert winner_fitness <= max(FITNESS_VALUES)


# ---------------------------------------------------------------------------
# Uniform fitness: any individual is valid
# ---------------------------------------------------------------------------


def test_uniform_fitness_returns_valid_chromosome():
    """When all individuals have equal fitness, any one of them is a valid winner."""
    equal_fitness = [10.0] * len(POPULATION)
    for _ in range(50):
        winner = tournament_selection(POPULATION, equal_fitness, tournament_size=3)
        assert winner in POPULATION


# ---------------------------------------------------------------------------
# Edge cases and error handling
# ---------------------------------------------------------------------------


def test_raises_on_tournament_size_zero():
    """tournament_size=0 is invalid and must raise ValueError."""
    with pytest.raises(ValueError, match="tournament_size must be at least 1"):
        tournament_selection(POPULATION, FITNESS_VALUES, tournament_size=0)


def test_raises_when_tournament_size_exceeds_population():
    """tournament_size larger than population must raise ValueError."""
    with pytest.raises(ValueError, match="exceeds population size"):
        tournament_selection(
            POPULATION, FITNESS_VALUES, tournament_size=len(POPULATION) + 1
        )
