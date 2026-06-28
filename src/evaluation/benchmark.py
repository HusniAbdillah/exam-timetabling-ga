import csv
import json
from pathlib import Path

from src.evaluation.greedy import run_greedy
from src.fitness.fitness import (
    calculate_fitness,
    evaluate_constraints,
    initialize_fitness_data,
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
    students, courses, enrollments, timeslots = load_dataset(DATA_DIR)
    validate_dataset(students, courses, enrollments, timeslots)

    # 2. Build conflict matrix
    conflict_matrix = build_conflict_matrix(enrollments, courses)

    # Convert Course/Timeslot list to primitives for GA engine
    course_ids = [c.course_id for c in courses]
    slot_ids = [t.slot_id for t in timeslots]

    # Initialize fitness registry
    initialize_fitness_data(students, courses, enrollments, timeslots)

    # 3. Run Genetic Algorithm
    ga_result = run_ga(
        course_ids,
        slot_ids,
        conflict_matrix,
        ga_config,
        calculate_fitness,
    )

    # 4. Run Greedy Baseline
    greedy_result = run_greedy(
        students,
        courses,
        enrollments,
        timeslots,
        conflict_matrix,
    )

    # 5. Evaluate final constraint statistics
    ga_stats = evaluate_constraints(ga_result.best_solution)
    greedy_stats = evaluate_constraints(greedy_result.best_solution)

    # Map timeslot ID for reporting
    timeslot_map = {t.slot_id: t for t in timeslots}

    # 6. Save outputs/schedule.csv (based on GA best solution)
    schedule_rows = []
    for idx, course in enumerate(courses):
        assigned_slot_id = ga_result.best_solution[idx]
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

    # 7. Save outputs/fitness_history.csv
    history_file = output_dir / "fitness_history.csv"
    with open(history_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["generation", "best_fitness"])
        for gen_idx, fitness_val in enumerate(ga_result.fitness_history):
            writer.writerow([gen_idx, fitness_val])

    # 8. Save outputs/statistics.json
    stats_data = {
        "ga": {
            "execution_time_seconds": ga_result.execution_time,
            "best_fitness": ga_result.best_fitness,
            "hard_constraint_violations": ga_stats["hard_constraint_violations"],
            "consecutive_exams_violations": ga_stats["consecutive_exams_violations"],
            "too_many_exams_violations": ga_stats["too_many_exams_violations"],
            "spread_penalty": ga_stats["spread_penalty"],
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
    }

    stats_file = output_dir / "statistics.json"
    with open(stats_file, mode="w", encoding="utf-8") as f:
        json.dump(stats_data, f, indent=2)


if __name__ == "__main__":
    run_benchmark()
