import json
from pathlib import Path

import plotly.graph_objects as go


def _load_stats(stats_or_path: dict | Path | str) -> dict:
    """Helper untuk memuat data statistik dari dictionary atau berkas path JSON.

    Args:
        stats_or_path: Objek dictionary statistik atau path menuju file JSON.

    Returns:
        dict: Dictionary statistik.
    """
    if isinstance(stats_or_path, (str, Path)):
        with open(stats_or_path, encoding="utf-8") as f:
            return json.load(f)
    return stats_or_path


def plot_fitness_comparison(stats_or_path: dict | Path | str) -> go.Figure:
    """Membuat diagram batang perbandingan nilai fitness akhir (Total Penalti)
    Pure GA vs Greedy vs Hybrid GA.

    Args:
        stats_or_path: Objek dictionary statistik atau path menuju file JSON.

    Returns:
        go.Figure: Objek grafik Plotly.
    """
    stats = _load_stats(stats_or_path)
    algorithms = ["Pure GA", "Greedy Baseline", "Hybrid GA (Greedy + GA)"]
    fitness_values = [
        stats["pure_ga"]["best_fitness"],
        stats["greedy"]["best_fitness"],
        stats["hybrid_ga"]["best_fitness"],
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=algorithms,
                y=fitness_values,
                marker_color=[
                    "#0ea5e9",
                    "#64748b",
                    "#4f46e5",
                ],  # Sky Blue, Slate Gray, Indigo
                text=[f"{val:.2f}" for val in fitness_values],
                textposition="auto",
                hovertemplate="Algoritma: %{x}<br>Total Penalti: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        yaxis_title="Total Penalti",
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=40),
        font=dict(family="Inter, sans-serif", color="#475569"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def plot_violations_comparison(stats_or_path: dict | Path | str) -> go.Figure:
    """Membuat diagram batang perbandingan pelanggaran constraint &
    penalti detail Pure GA vs Greedy vs Hybrid GA.

    Args:
        stats_or_path: Objek dictionary statistik atau path menuju file JSON.

    Returns:
        go.Figure: Objek grafik Plotly.
    """
    stats = _load_stats(stats_or_path)
    categories = [
        "Hard Constraint",
        "Consecutive Exams",
        "Too Many Exams / Day",
        "Spread Penalty",
    ]

    pure_ga_vals = [
        stats["pure_ga"]["hard_constraint_violations"],
        stats["pure_ga"]["consecutive_exams_violations"],
        stats["pure_ga"]["too_many_exams_violations"],
        stats["pure_ga"]["spread_penalty"],
    ]

    greedy_vals = [
        stats["greedy"]["hard_constraint_violations"],
        stats["greedy"]["consecutive_exams_violations"],
        stats["greedy"]["too_many_exams_violations"],
        stats["greedy"]["spread_penalty"],
    ]

    hybrid_ga_vals = [
        stats["hybrid_ga"]["hard_constraint_violations"],
        stats["hybrid_ga"]["consecutive_exams_violations"],
        stats["hybrid_ga"]["too_many_exams_violations"],
        stats["hybrid_ga"]["spread_penalty"],
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                name="Pure GA",
                x=categories,
                y=pure_ga_vals,
                marker_color="#0ea5e9",
            ),
            go.Bar(
                name="Greedy Baseline",
                x=categories,
                y=greedy_vals,
                marker_color="#64748b",
            ),
            go.Bar(
                name="Hybrid GA (Greedy + GA)",
                x=categories,
                y=hybrid_ga_vals,
                marker_color="#4f46e5",
            ),
        ]
    )

    fig.update_layout(
        barmode="group",
        yaxis_title="Jumlah Pelanggaran / Nilai Penalti",
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=40),
        font=dict(family="Inter, sans-serif", color="#475569"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
