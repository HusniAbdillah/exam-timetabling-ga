import csv
import json
import math
import random

import matplotlib.pyplot as plt

from src.evaluation.greedy import run_greedy
from src.fitness.fitness import (
    calculate_fitness,
    initialize_fitness_data,
)
from src.ga.engine import GAConfig, run_ga
from src.preprocessing.conflict_matrix import build_conflict_matrix
from src.preprocessing.load_dataset import load_dataset
from src.preprocessing.validator import validate_dataset
from src.utils.constants import DATA_DIR, OUTPUT_DIR


def run_sensitivity_analysis(
    students, courses, enrollments, timeslots, conflict_matrix, course_ids, slot_ids
) -> None:
    """Run GA with varying parameters to analyze convergence characteristics."""
    print("\n--- Running Experiment 1: Sensitivity Analysis ---")
    pop_sizes = [50, 100, 150]
    mutation_rates = [0.01, 0.05, 0.1, 0.2]
    max_gens = 50

    results = []

    # Test each combination of population size and mutation rate
    for pop in pop_sizes:
        for p_mut in mutation_rates:
            print(f"Testing Pop Size: {pop}, Mutation Rate: {p_mut}...")
            random.seed(42)  # Control seed for direct comparison

            config = GAConfig(
                population_size=pop,
                max_generations=max_gens,
                crossover_rate=0.8,
                mutation_rate=p_mut,
            )

            ga_result = run_ga(
                course_ids,
                slot_ids,
                conflict_matrix,
                config,
                calculate_fitness,
            )

            # Record fitness value at generations 0, 10, 20, 30, 40, 50
            history = ga_result.fitness_history
            record = {
                "population_size": pop,
                "mutation_rate": p_mut,
                "gen_0": history[0] if len(history) > 0 else None,
                "gen_10": history[10] if len(history) > 10 else None,
                "gen_20": history[20] if len(history) > 20 else None,
                "gen_30": history[30] if len(history) > 30 else None,
                "gen_40": history[40] if len(history) > 40 else None,
                "gen_50": history[-1] if len(history) > 0 else None,
                "best_fitness": ga_result.best_fitness,
            }
            results.append(record)

    # Save to outputs/sensitivity_analysis.csv
    csv_file = OUTPUT_DIR / "sensitivity_analysis.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved sensitivity analysis data to: {csv_file}")

    # Plot and save sensitivity analysis
    plt.figure(figsize=(10, 6))
    for r in results:
        gens = [0, 10, 20, 30, 40, 50]
        fitness = [r[f"gen_{g}"] for g in gens if r[f"gen_{g}"] is not None]
        x_vals = gens[: len(fitness)]
        plt.plot(
            x_vals,
            fitness,
            marker="o",
            label=f"Pop={r['population_size']}, Mut={r['mutation_rate']}",
        )
    plt.title("Analisis Sensitivitas - Konvergensi Algoritma Genetika")
    plt.xlabel("Generasi")
    plt.ylabel("Fitness (Total Penalti)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    png_file = OUTPUT_DIR / "sensitivity_analysis.png"
    plt.savefig(png_file, dpi=300)
    plt.close()
    print(f"Saved sensitivity analysis plot to: {png_file}")


def run_statistical_significance(
    students, courses, enrollments, timeslots, conflict_matrix, course_ids, slot_ids
) -> None:
    """Run GA 30 times with different seeds to measure stochastic robustness."""
    print("\n--- Running Experiment 2: Statistical Significance (30 Runs) ---")
    fitness_results = []
    time_results = []
    num_runs = 30

    config = GAConfig(
        population_size=50,
        max_generations=50,
        crossover_rate=0.8,
        mutation_rate=0.1,
    )

    for run in range(1, num_runs + 1):
        print(f"Run {run}/{num_runs}...")
        random.seed(run)  # Vary the seed for each independent run

        ga_result = run_ga(
            course_ids,
            slot_ids,
            conflict_matrix,
            config,
            calculate_fitness,
        )
        fitness_results.append(ga_result.best_fitness)
        time_results.append(ga_result.execution_time)

    # Calculate metrics
    mean_fitness = sum(fitness_results) / num_runs
    best_fitness = min(fitness_results)
    worst_fitness = max(fitness_results)
    std_dev_fitness = math.sqrt(
        sum((x - mean_fitness) ** 2 for x in fitness_results) / num_runs
    )

    mean_time = sum(time_results) / num_runs
    total_time = sum(time_results)

    stats_report = {
        "number_of_runs": num_runs,
        "fitness": {
            "best_value": best_fitness,
            "worst_value": worst_fitness,
            "mean_value": mean_fitness,
            "standard_deviation": std_dev_fitness,
        },
        "time_seconds": {
            "total_execution_time": total_time,
            "mean_execution_time": mean_time,
        },
        "raw_runs": [
            {"run": idx + 1, "fitness": f, "time_seconds": t}
            for idx, (f, t) in enumerate(
                zip(fitness_results, time_results, strict=True)
            )
        ],
    }

    # Save to outputs/statistical_significance.json
    json_file = OUTPUT_DIR / "statistical_significance.json"
    with open(json_file, mode="w", encoding="utf-8") as f:
        json.dump(stats_report, f, indent=2)
    print(f"Saved statistical robustness data to: {json_file}")


def run_time_complexity_profile(
    students, courses, enrollments, timeslots, conflict_matrix
) -> None:
    """Compare execution time complexity of GA vs Greedy."""
    print("\n--- Running Experiment 3: Time Complexity Profiling ---")

    # Measure Greedy Baseline time
    greedy_result = run_greedy(
        students, courses, enrollments, timeslots, conflict_matrix
    )
    greedy_time = greedy_result.execution_time
    print(f"Greedy Solver execution time: {greedy_time:.4f} seconds")

    # Measure GA execution time for varying generations
    course_ids = [c.course_id for c in courses]
    slot_ids = [t.slot_id for t in timeslots]
    generations_steps = [5, 10, 20, 40]

    ga_profiles = []
    for gens in generations_steps:
        config = GAConfig(
            population_size=50,
            max_generations=gens,
            crossover_rate=0.8,
            mutation_rate=0.1,
        )
        random.seed(42)
        ga_result = run_ga(
            course_ids,
            slot_ids,
            conflict_matrix,
            config,
            calculate_fitness,
        )
        ga_profiles.append(
            {
                "generations": gens,
                "population_size": 50,
                "execution_time_seconds": ga_result.execution_time,
                "fitness": ga_result.best_fitness,
            }
        )
        print(f"GA ({gens} gens) time: {ga_result.execution_time:.4f}s")

    profile_report = {
        "greedy": {
            "execution_time_seconds": greedy_time,
            "fitness": greedy_result.best_fitness,
        },
        "ga_scaling": ga_profiles,
    }

    # Save to outputs/time_complexity_profile.json
    json_file = OUTPUT_DIR / "time_complexity_profile.json"
    with open(json_file, mode="w", encoding="utf-8") as f:
        json.dump(profile_report, f, indent=2)
    print(f"Saved execution time complexity profiles to: {json_file}")

    # Plot and save complexity comparison
    plt.figure(figsize=(8, 5))
    gens = [p["generations"] for p in ga_profiles]
    times = [p["execution_time_seconds"] for p in ga_profiles]

    plt.plot(
        gens,
        times,
        marker="s",
        color="#4f46e5",
        linewidth=2,
        label="Genetic Algorithm",
    )
    plt.axhline(
        y=greedy_time,
        color="#64748b",
        linestyle="--",
        linewidth=2,
        label="Greedy Baseline",
    )

    plt.title("Profil Kompleksitas Waktu - GA vs Greedy")
    plt.xlabel("Jumlah Generasi (Ukuran Populasi = 50)")
    plt.ylabel("Waktu Eksekusi (Detik)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    png_file = OUTPUT_DIR / "time_complexity_profile.png"
    plt.savefig(png_file, dpi=300)
    plt.close()
    print(f"Saved time complexity plot to: {png_file}")


def main() -> None:
    """Execute the three academic research experiments."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    students, courses, enrollments, timeslots = load_dataset(DATA_DIR)
    validate_dataset(students, courses, enrollments, timeslots)

    # 2. Build conflicts
    conflict_matrix = build_conflict_matrix(enrollments, courses)

    # 3. Setup fitness registry
    initialize_fitness_data(students, courses, enrollments, timeslots)

    course_ids = [c.course_id for c in courses]
    slot_ids = [t.slot_id for t in timeslots]

    # Run Experiments
    run_sensitivity_analysis(
        students, courses, enrollments, timeslots, conflict_matrix, course_ids, slot_ids
    )
    run_statistical_significance(
        students, courses, enrollments, timeslots, conflict_matrix, course_ids, slot_ids
    )
    run_time_complexity_profile(
        students, courses, enrollments, timeslots, conflict_matrix
    )

    print("\nAll academic experiments completed successfully!")


if __name__ == "__main__":
    main()
