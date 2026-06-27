from src.ga.mutation import move_mutation, swap_mutation

# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

CHROMOSOME = [1, 3, 2, 5, 4, 1, 3]
NUM_TIMESLOTS = 5


# ---------------------------------------------------------------------------
# swap_mutation — structural invariants
# ---------------------------------------------------------------------------


def test_swap_preserves_length():
    """Mutated chromosome must have the same length as the original."""
    mutated = swap_mutation(CHROMOSOME, mutation_rate=0.9)
    assert len(mutated) == len(CHROMOSOME)


def test_swap_returns_new_object():
    """swap_mutation must not modify the original chromosome in-place."""
    original = CHROMOSOME[:]
    swap_mutation(original, mutation_rate=1.0)
    assert original == CHROMOSOME


def test_swap_rate_zero_no_change():
    """With mutation_rate=0.0, swap_mutation must never alter the chromosome."""
    for _ in range(100):
        mutated = swap_mutation(CHROMOSOME, mutation_rate=0.0)
        assert mutated == CHROMOSOME


def test_swap_rate_one_preserves_multiset():
    """swap_mutation only reorders values — the sorted result must be identical."""
    for _ in range(50):
        mutated = swap_mutation(CHROMOSOME, mutation_rate=1.0)
        assert sorted(mutated) == sorted(CHROMOSOME)


def test_swap_single_gene_chromosome_unchanged():
    """A chromosome with a single gene cannot be swapped — result equals input."""
    single = [3]
    for _ in range(20):
        mutated = swap_mutation(single, mutation_rate=1.0)
        assert mutated == single


# ---------------------------------------------------------------------------
# swap_mutation — value integrity
# ---------------------------------------------------------------------------


def test_swap_values_remain_from_original():
    """Every value in the mutated chromosome must appear in the original."""
    original_values = set(CHROMOSOME)
    for _ in range(50):
        mutated = swap_mutation(CHROMOSOME, mutation_rate=1.0)
        assert set(mutated) <= original_values


# ---------------------------------------------------------------------------
# move_mutation — structural invariants
# ---------------------------------------------------------------------------


def test_move_preserves_length():
    """Mutated chromosome must have the same length as the original."""
    mutated = move_mutation(CHROMOSOME, NUM_TIMESLOTS, mutation_rate=0.5)
    assert len(mutated) == len(CHROMOSOME)


def test_move_returns_new_object():
    """move_mutation must not modify the original chromosome in-place."""
    original = CHROMOSOME[:]
    move_mutation(original, NUM_TIMESLOTS, mutation_rate=1.0)
    assert original == CHROMOSOME


def test_move_rate_zero_no_change():
    """With mutation_rate=0.0, move_mutation must not change any gene."""
    mutated = move_mutation(CHROMOSOME, NUM_TIMESLOTS, mutation_rate=0.0)
    assert mutated == CHROMOSOME


# ---------------------------------------------------------------------------
# move_mutation — value range
# ---------------------------------------------------------------------------


def test_move_values_in_valid_range():
    """All gene values after move_mutation must lie within [1, num_timeslots]."""
    for _ in range(50):
        mutated = move_mutation(CHROMOSOME, NUM_TIMESLOTS, mutation_rate=0.8)
        assert all(1 <= gene <= NUM_TIMESLOTS for gene in mutated)


def test_move_rate_one_values_in_valid_range():
    """With mutation_rate=1.0, every gene is reassigned but must still be in range."""
    mutated = move_mutation(CHROMOSOME, NUM_TIMESLOTS, mutation_rate=1.0)
    assert all(1 <= gene <= NUM_TIMESLOTS for gene in mutated)


# ---------------------------------------------------------------------------
# move_mutation — mutation actually occurs at high rates
# ---------------------------------------------------------------------------


def test_move_high_rate_changes_at_least_one_gene():
    """With mutation_rate=1.0 and many genes, at least one gene should differ.

    Each gene is independently reassigned to randint(1, num_timeslots).
    P(all 20 genes stay the same when num_timeslots=5) = (1/5)^20 ≈ 10^-14,
    making this test effectively deterministic.
    """
    long_chromosome = [1] * 20
    changed_at_least_once = False

    for _ in range(10):
        mutated = move_mutation(long_chromosome, num_timeslots=5, mutation_rate=1.0)
        if mutated != long_chromosome:
            changed_at_least_once = True
            break

    assert changed_at_least_once
