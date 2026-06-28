import csv
import json
import math
import random

import matplotlib.pyplot as plt

from src.evaluation.greedy import run_greedy
from src.fitness.fitness import (
    calculate_fitness,
    initialize_fitness_data,
    set_blocked_slots,
    set_room_data,
)
from src.ga.engine import GAConfig, run_ga
from src.preprocessing.conflict_matrix import build_conflict_matrix
from src.preprocessing.load_dataset import load_dataset
from src.preprocessing.validator import validate_dataset
from src.utils.constants import DATA_DIR, OUTPUT_DIR


def run_sensitivity_analysis(
    students, courses, enrollments, timeslots, conflict_matrix, course_ids, slot_ids
) -> None:
    """Run Pure GA and Hybrid GA with varying parameters to analyze convergence characteristics."""
    print("\n--- Running Experiment 1: Sensitivity Analysis (Pure GA & Hybrid GA) ---")
    pop_sizes = [50, 100]
    mutation_rates = [0.01, 0.05, 0.1, 0.2]
    max_gens = 50

    # Get Greedy seed
    greedy_res = run_greedy(students, courses, enrollments, timeslots, conflict_matrix)
    greedy_sol = greedy_res.best_solution

    results = []

    # Test each combination of population size and mutation rate
    for pop in pop_sizes:
        for p_mut in mutation_rates:
            print(f"Testing Pop Size: {pop}, Mutation Rate: {p_mut}...")

            # 1. Pure GA
            random.seed(42)
            pure_config = GAConfig(
                population_size=pop,
                max_generations=max_gens,
                crossover_rate=0.8,
                mutation_rate=p_mut,
                enable_repair=False,
            )
            pure_res = run_ga(
                course_ids,
                slot_ids,
                conflict_matrix,
                pure_config,
                calculate_fitness,
                seeds=None,
            )
            history_pure = pure_res.fitness_history
            results.append(
                {
                    "algorithm": "Pure GA",
                    "population_size": pop,
                    "mutation_rate": p_mut,
                    "gen_0": history_pure[0] if len(history_pure) > 0 else None,
                    "gen_10": history_pure[10] if len(history_pure) > 10 else None,
                    "gen_20": history_pure[20] if len(history_pure) > 20 else None,
                    "gen_30": history_pure[30] if len(history_pure) > 30 else None,
                    "gen_40": history_pure[40] if len(history_pure) > 40 else None,
                    "gen_50": history_pure[-1] if len(history_pure) > 0 else None,
                    "best_fitness": pure_res.best_fitness,
                }
            )

            # 2. Hybrid GA
            random.seed(42)
            hybrid_config = GAConfig(
                population_size=pop,
                max_generations=max_gens,
                crossover_rate=0.8,
                mutation_rate=p_mut,
                enable_repair=True,
            )
            hybrid_res = run_ga(
                course_ids,
                slot_ids,
                conflict_matrix,
                hybrid_config,
                calculate_fitness,
                seeds=[greedy_sol],
            )
            history_hybrid = hybrid_res.fitness_history
            results.append(
                {
                    "algorithm": "Hybrid GA",
                    "population_size": pop,
                    "mutation_rate": p_mut,
                    "gen_0": history_hybrid[0] if len(history_hybrid) > 0 else None,
                    "gen_10": history_hybrid[10] if len(history_hybrid) > 10 else None,
                    "gen_20": history_hybrid[20] if len(history_hybrid) > 20 else None,
                    "gen_30": history_hybrid[30] if len(history_hybrid) > 30 else None,
                    "gen_40": history_hybrid[40] if len(history_hybrid) > 40 else None,
                    "gen_50": history_hybrid[-1] if len(history_hybrid) > 0 else None,
                    "best_fitness": hybrid_res.best_fitness,
                }
            )

    # Save to outputs/sensitivity_analysis.csv
    csv_file = OUTPUT_DIR / "sensitivity_analysis.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved sensitivity analysis data to: {csv_file}")

    # Plot and save sensitivity analysis (2 subplots)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Pure GA
    axes[0].set_title("Sensitivitas Konvergensi - Pure GA")
    axes[0].set_xlabel("Generasi")
    axes[0].set_ylabel("Fitness (Total Penalti)")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    # Subplot 2: Hybrid GA
    axes[1].set_title("Sensitivitas Konvergensi - Hybrid GA")
    axes[1].set_xlabel("Generasi")
    axes[1].set_ylabel("Fitness (Total Penalti)")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    for r in results:
        gens = [0, 10, 20, 30, 40, 50]
        fitness = [r[f"gen_{g}"] for g in gens if r[f"gen_{g}"] is not None]
        x_vals = gens[: len(fitness)]

        lbl = f"Pop={r['population_size']}, Mut={r['mutation_rate']}"
        if r["algorithm"] == "Pure GA":
            axes[0].plot(x_vals, fitness, marker="o", label=lbl)
        else:
            axes[1].plot(x_vals, fitness, marker="s", label=lbl)

    axes[0].legend(loc="upper right")
    axes[1].legend(loc="upper right")

    plt.tight_layout()
    png_file = OUTPUT_DIR / "sensitivity_analysis.png"
    plt.savefig(png_file, dpi=300)
    plt.close()
    print(f"Saved sensitivity analysis plot to: {png_file}")


def run_statistical_significance(
    students, courses, enrollments, timeslots, conflict_matrix, course_ids, slot_ids
) -> None:
    """Run Pure GA vs Hybrid GA 30 times with different seeds to measure stochastic robustness."""
    print("\n--- Running Experiment 2: Statistical Significance (30 Runs) ---")
    pure_fitness = []
    pure_time = []
    hybrid_fitness = []
    hybrid_time = []
    num_runs = 30

    config = GAConfig(
        population_size=50,
        max_generations=50,
        crossover_rate=0.8,
        mutation_rate=0.1,
    )

    # Run Greedy once
    greedy_res = run_greedy(students, courses, enrollments, timeslots, conflict_matrix)
    greedy_sol = greedy_res.best_solution
    greedy_fit = greedy_res.best_fitness

    for run in range(1, num_runs + 1):
        print(f"Run {run}/{num_runs}...")

        # Pure GA
        random.seed(run)
        pure_res = run_ga(
            course_ids,
            slot_ids,
            conflict_matrix,
            config,
            calculate_fitness,
            seeds=None,
        )
        pure_fitness.append(pure_res.best_fitness)
        pure_time.append(pure_res.execution_time)

        # Hybrid GA (with repair enabled)
        random.seed(run)
        import copy

        hybrid_config = copy.deepcopy(config)
        hybrid_config.enable_repair = True

        hybrid_res = run_ga(
            course_ids,
            slot_ids,
            conflict_matrix,
            hybrid_config,
            calculate_fitness,
            seeds=[greedy_sol],
        )
        hybrid_fitness.append(hybrid_res.best_fitness)
        hybrid_time.append(hybrid_res.execution_time)

    # Calculate metrics for Pure GA
    pure_mean = sum(pure_fitness) / num_runs
    pure_std = math.sqrt(sum((x - pure_mean) ** 2 for x in pure_fitness) / num_runs)
    pure_mean_time = sum(pure_time) / num_runs

    # Calculate metrics for Hybrid GA
    hybrid_mean = sum(hybrid_fitness) / num_runs
    hybrid_std = math.sqrt(
        sum((x - hybrid_mean) ** 2 for x in hybrid_fitness) / num_runs
    )
    hybrid_mean_time = sum(hybrid_time) / num_runs

    stats_report = {
        "number_of_runs": num_runs,
        "greedy_baseline": {
            "fitness": greedy_fit,
            "execution_time_seconds": greedy_res.execution_time,
        },
        "pure_ga": {
            "best_value": min(pure_fitness),
            "worst_value": max(pure_fitness),
            "mean_value": pure_mean,
            "standard_deviation": pure_std,
            "mean_execution_time_seconds": pure_mean_time,
        },
        "hybrid_ga": {
            "best_value": min(hybrid_fitness),
            "worst_value": max(hybrid_fitness),
            "mean_value": hybrid_mean,
            "standard_deviation": hybrid_std,
            "mean_execution_time_seconds": hybrid_mean_time,
        },
        "raw_runs": [
            {
                "run": idx + 1,
                "pure_ga_fitness": pf,
                "pure_ga_time": pt,
                "hybrid_ga_fitness": hf,
                "hybrid_ga_time": ht,
            }
            for idx, (pf, pt, hf, ht) in enumerate(
                zip(pure_fitness, pure_time, hybrid_fitness, hybrid_time, strict=True)
            )
        ],
    }

    # Save to outputs/statistical_significance.json
    json_file = OUTPUT_DIR / "statistical_significance.json"
    with open(json_file, mode="w", encoding="utf-8") as f:
        json.dump(stats_report, f, indent=2)
    print(f"Saved statistical robustness data to: {json_file}")

    # Plot boxplot for statistical significance
    plt.figure(figsize=(8, 6))
    data_to_plot = [pure_fitness, hybrid_fitness]
    plt.boxplot(data_to_plot, labels=["Pure GA", "Hybrid GA"])
    plt.axhline(
        y=greedy_fit,
        color="#ef4444",
        linestyle="--",
        linewidth=2,
        label=f"Greedy Baseline ({greedy_fit:.1f})",
    )
    plt.title("Signifikansi Statistik (30 Runs) - Kualitas Solusi (Fitness)")
    plt.ylabel("Total Penalti (Lebih Rendah Lebih Baik)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    png_file = OUTPUT_DIR / "statistical_significance.png"
    plt.savefig(png_file, dpi=300)
    plt.close()
    print(f"Saved statistical significance boxplot to: {png_file}")


def run_time_complexity_profile(
    students, courses, enrollments, timeslots, conflict_matrix
) -> None:
    """Compare execution time complexity of Pure GA, Greedy, and Hybrid GA."""
    print("\n--- Running Experiment 3: Time Complexity Profiling ---")

    # Measure Greedy Baseline time
    greedy_result = run_greedy(
        students, courses, enrollments, timeslots, conflict_matrix
    )
    greedy_time = greedy_result.execution_time
    greedy_sol = greedy_result.best_solution
    print(f"Greedy Solver execution time: {greedy_time:.4f} seconds")

    # Measure execution time for varying generations
    course_ids = [c.course_id for c in courses]
    slot_ids = [t.slot_id for t in timeslots]
    generations_steps = [5, 10, 20, 40]

    pure_profiles = []
    hybrid_profiles = []

    for gens in generations_steps:
        config = GAConfig(
            population_size=50,
            max_generations=gens,
            crossover_rate=0.8,
            mutation_rate=0.1,
        )

        # Pure GA
        random.seed(42)
        pure_res = run_ga(
            course_ids,
            slot_ids,
            conflict_matrix,
            config,
            calculate_fitness,
            seeds=None,
        )
        pure_profiles.append(
            {
                "generations": gens,
                "execution_time_seconds": pure_res.execution_time,
                "fitness": pure_res.best_fitness,
            }
        )

        # Hybrid GA (with repair enabled)
        random.seed(42)
        import copy

        hybrid_config = copy.deepcopy(config)
        hybrid_config.enable_repair = True

        hybrid_res = run_ga(
            course_ids,
            slot_ids,
            conflict_matrix,
            hybrid_config,
            calculate_fitness,
            seeds=[greedy_sol],
        )
        hybrid_profiles.append(
            {
                "generations": gens,
                "execution_time_seconds": hybrid_res.execution_time,
                "fitness": hybrid_res.best_fitness,
            }
        )
        print(
            f"Gens {gens}: Pure Time={pure_res.execution_time:.4f}s, Hybrid Time={hybrid_res.execution_time:.4f}s"
        )

    profile_report = {
        "greedy": {
            "execution_time_seconds": greedy_time,
            "fitness": greedy_result.best_fitness,
        },
        "pure_ga": pure_profiles,
        "hybrid_ga": hybrid_profiles,
    }

    # Save to outputs/time_complexity_profile.json
    json_file = OUTPUT_DIR / "time_complexity_profile.json"
    with open(json_file, mode="w", encoding="utf-8") as f:
        json.dump(profile_report, f, indent=2)
    print(f"Saved execution time complexity profiles to: {json_file}")

    # Plot and save complexity comparison
    plt.figure(figsize=(8, 5))
    gens = [p["generations"] for p in pure_profiles]

    pure_times = [p["execution_time_seconds"] for p in pure_profiles]
    hybrid_times = [p["execution_time_seconds"] for p in hybrid_profiles]

    plt.plot(
        gens,
        pure_times,
        marker="o",
        color="#0ea5e9",
        linewidth=2,
        label="Pure GA",
    )
    plt.plot(
        gens,
        hybrid_times,
        marker="s",
        color="#4f46e5",
        linewidth=2,
        label="Hybrid GA (Greedy + GA)",
    )
    plt.axhline(
        y=greedy_time,
        color="#64748b",
        linestyle="--",
        linewidth=2,
        label="Greedy Baseline",
    )

    plt.title("Profil Kompleksitas Waktu - Pure GA vs Greedy vs Hybrid GA")
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
    import argparse

    parser = argparse.ArgumentParser(description="Jalankan Eksperimen Akademik GA.")
    parser.add_argument(
        "--exp",
        choices=["1", "2", "3", "all"],
        default=None,
        help="Nomor eksperimen yang ingin dijalankan (1: Sensitivitas, 2: Signifikansi Statistik, 3: Kompleksitas Waktu, all: Semua)",
    )
    args = parser.parse_args()

    choice = args.exp
    if choice is None:
        print("\nPilih eksperimen yang ingin dijalankan:")
        print("1. Eksperimen 1: Analisis Sensitivitas (Pure GA vs Hybrid GA)")
        print("2. Eksperimen 2: Signifikansi Statistik (30 Runs)")
        print("3. Eksperimen 3: Profil Kompleksitas Waktu")
        print("4. Jalankan Semua Eksperimen")
        ans = input("Masukkan pilihan (1/2/3/4): ").strip()
        if ans == "1":
            choice = "1"
        elif ans == "2":
            choice = "2"
        elif ans == "3":
            choice = "3"
        else:
            choice = "all"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    students, courses, enrollments, timeslots, rooms, slot_blocks = load_dataset(
        DATA_DIR
    )
    # Register additional data for fitness calculations
    set_room_data(rooms, {c.course_id: c.room_id for c in courses if c.room_id})
    set_blocked_slots(slot_blocks)
    validate_dataset(students, courses, enrollments, timeslots)

    # 2. Build conflicts
    conflict_matrix = build_conflict_matrix(enrollments, courses)

    # 3. Setup fitness registry
    initialize_fitness_data(students, courses, enrollments, timeslots)

    course_ids = [c.course_id for c in courses]
    slot_ids = [t.slot_id for t in timeslots]

    # Run selected experiments
    if choice in ["1", "all"]:
        run_sensitivity_analysis(
            students,
            courses,
            enrollments,
            timeslots,
            conflict_matrix,
            course_ids,
            slot_ids,
        )
    if choice in ["2", "all"]:
        run_statistical_significance(
            students,
            courses,
            enrollments,
            timeslots,
            conflict_matrix,
            course_ids,
            slot_ids,
        )
    if choice in ["3", "all"]:
        run_time_complexity_profile(
            students, courses, enrollments, timeslots, conflict_matrix
        )

    print("\nPembentukan grafik dan analisis eksperimen selesai!")


if __name__ == "__main__":
    main()
