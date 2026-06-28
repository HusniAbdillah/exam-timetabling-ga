import csv
import json
from pathlib import Path

from src.evaluation.greedy import run_greedy
from src.fitness.fitness import (
    calculate_fitness,
    evaluate_constraints,
    initialize_fitness_data,
    set_blocked_slots,
    set_room_data,
)
from src.ga.engine import GAConfig, run_ga
from src.preprocessing.conflict_matrix import build_conflict_matrix
from src.preprocessing.load_dataset import load_dataset
from src.preprocessing.validator import validate_dataset
from src.utils.constants import DATA_DIR, OUTPUT_DIR


def run_benchmark(
    ga_config: GAConfig | None = None,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    """Run the complete optimization benchmark comparing GA vs Greedy.

    Loads the dataset, validates it, runs both GA and Greedy algorithms,
    and writes results to outputs/.

    Args:
        ga_config: Configurations/hyperparameters for the GA engine.
        output_dir: Path to export outputs.
    """
    if ga_config is None:
        ga_config = GAConfig()

    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load and validate data
    students, courses, enrollments, timeslots, rooms, slot_blocks = load_dataset(
        DATA_DIR
    )
    # Register additional data for fitness calculations
    set_room_data(rooms, {c.course_id: c.room_id for c in courses if c.room_id})
    set_blocked_slots(slot_blocks)
    validate_dataset(students, courses, enrollments, timeslots)

    # 2. Build conflict matrix
    conflict_matrix = build_conflict_matrix(enrollments, courses)

    # Convert Course/Timeslot list to primitives for GA engine
    course_ids = [c.course_id for c in courses]
    slot_ids = [t.slot_id for t in timeslots]

    # Initialize fitness registry
    initialize_fitness_data(students, courses, enrollments, timeslots)

    # 3. Run Greedy Baseline
    greedy_result = run_greedy(
        students,
        courses,
        enrollments,
        timeslots,
        conflict_matrix,
    )

    # 4. Run Pure Genetic Algorithm (no seed)
    pure_ga_result = run_ga(
        course_ids,
        slot_ids,
        conflict_matrix,
        ga_config,
        calculate_fitness,
        seeds=None,
    )

    # 5. Run Hybrid Genetic Algorithm (seeded with Greedy solution and with Repair enabled)
    import copy

    hybrid_config = copy.deepcopy(ga_config)
    hybrid_config.enable_repair = True

    hybrid_ga_result = run_ga(
        course_ids,
        slot_ids,
        conflict_matrix,
        hybrid_config,
        calculate_fitness,
        seeds=[greedy_result.best_solution],
    )

    # 6. Evaluate final constraint statistics
    pure_ga_stats = evaluate_constraints(pure_ga_result.best_solution)
    greedy_stats = evaluate_constraints(greedy_result.best_solution)
    hybrid_ga_stats = evaluate_constraints(hybrid_ga_result.best_solution)

    # Map timeslot ID for reporting
    timeslot_map = {t.slot_id: t for t in timeslots}

    # 7. Save outputs/schedule.csv (based on Hybrid GA best solution)
    schedule_rows = []
    for idx, course in enumerate(courses):
        assigned_slot_id = hybrid_ga_result.best_solution[idx]
        ts = timeslot_map.get(assigned_slot_id)
        day = ts.day if ts else 1
        session = ts.session if ts else 1

        schedule_rows.append(
            {
                "course_id": course.course_id,
                "course_name": course.course_name,
                "slot_id": assigned_slot_id,
                "day": day,
                "session": session,
            }
        )

    schedule_file = output_dir / "schedule.csv"
    with open(schedule_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "course_id",
                "course_name",
                "slot_id",
                "day",
                "session",
            ],
        )
        writer.writeheader()
        writer.writerows(schedule_rows)

    # 8. Save outputs/fitness_history.csv (Pure GA vs Hybrid GA)
    history_file = output_dir / "fitness_history.csv"
    with open(history_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["generation", "pure_ga_fitness", "hybrid_ga_fitness"])
        max_len = max(
            len(pure_ga_result.fitness_history), len(hybrid_ga_result.fitness_history)
        )
        for gen_idx in range(max_len):
            p_val = (
                pure_ga_result.fitness_history[gen_idx]
                if gen_idx < len(pure_ga_result.fitness_history)
                else pure_ga_result.best_fitness
            )
            h_val = (
                hybrid_ga_result.fitness_history[gen_idx]
                if gen_idx < len(hybrid_ga_result.fitness_history)
                else hybrid_ga_result.best_fitness
            )
            writer.writerow([gen_idx, p_val, h_val])

    # 9. Save outputs/statistics.json (Pure GA, Greedy, Hybrid GA)
    stats_data = {
        "pure_ga": {
            "execution_time_seconds": pure_ga_result.execution_time,
            "best_fitness": pure_ga_result.best_fitness,
            "hard_constraint_violations": pure_ga_stats["hard_constraint_violations"],
            "consecutive_exams_violations": pure_ga_stats[
                "consecutive_exams_violations"
            ],
            "too_many_exams_violations": pure_ga_stats["too_many_exams_violations"],
            "spread_penalty": pure_ga_stats["spread_penalty"],
        },
        "greedy": {
            "execution_time_seconds": greedy_result.execution_time,
            "best_fitness": greedy_result.best_fitness,
            "hard_constraint_violations": greedy_stats["hard_constraint_violations"],
            "consecutive_exams_violations": greedy_stats[
                "consecutive_exams_violations"
            ],
            "too_many_exams_violations": greedy_stats["too_many_exams_violations"],
            "spread_penalty": greedy_stats["spread_penalty"],
        },
        "hybrid_ga": {
            "execution_time_seconds": hybrid_ga_result.execution_time,
            "best_fitness": hybrid_ga_result.best_fitness,
            "hard_constraint_violations": hybrid_ga_stats["hard_constraint_violations"],
            "consecutive_exams_violations": hybrid_ga_stats[
                "consecutive_exams_violations"
            ],
            "too_many_exams_violations": hybrid_ga_stats["too_many_exams_violations"],
            "spread_penalty": hybrid_ga_stats["spread_penalty"],
        },
    }

    stats_file = output_dir / "statistics.json"
    with open(stats_file, mode="w", encoding="utf-8") as f:
        json.dump(stats_data, f, indent=2)


if __name__ == "__main__":
    run_benchmark()
