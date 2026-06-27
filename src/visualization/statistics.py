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
    GA vs Greedy.

    Args:
        stats_or_path: Objek dictionary statistik atau path menuju file JSON.

    Returns:
        go.Figure: Objek grafik Plotly.
    """
    stats = _load_stats(stats_or_path)
    algorithms = ["Genetic Algorithm", "Greedy Baseline"]
    fitness_values = [stats["ga"]["best_fitness"], stats["greedy"]["best_fitness"]]

    fig = go.Figure(
        data=[
            go.Bar(
                x=algorithms,
                y=fitness_values,
                marker_color=["#3b82f6", "#94a3b8"],  # Blue vs Slate Gray
                text=fitness_values,
                textposition="auto",
                hovertemplate="Algoritma: %{x}<br>Total Penalti: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Perbandingan Kualitas Solusi (Lebih Rendah Lebih Baik)",
        yaxis_title="Total Penalti",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        title_font=dict(size=16, family="Outfit, Inter, sans-serif", color="#1e293b"),
        font=dict(family="Inter, sans-serif", color="#475569"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def plot_violations_comparison(stats_or_path: dict | Path | str) -> go.Figure:
    """Membuat diagram batang perbandingan pelanggaran constraint &
    penalti detail GA vs Greedy.

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

    ga_vals = [
        stats["ga"]["hard_constraint_violations"],
        stats["ga"]["consecutive_exams_violations"],
        stats["ga"]["too_many_exams_violations"],
        stats["ga"]["spread_penalty"],
    ]

    greedy_vals = [
        stats["greedy"]["hard_constraint_violations"],
        stats["greedy"]["consecutive_exams_violations"],
        stats["greedy"]["too_many_exams_violations"],
        stats["greedy"]["spread_penalty"],
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                name="Genetic Algorithm",
                x=categories,
                y=ga_vals,
                marker_color="#3b82f6",
            ),
            go.Bar(
                name="Greedy Baseline",
                x=categories,
                y=greedy_vals,
                marker_color="#94a3b8",
            ),
        ]
    )

    fig.update_layout(
        barmode="group",
        title="Perbandingan Detail Pelanggaran & Penalti",
        yaxis_title="Jumlah Pelanggaran / Nilai Penalti",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        title_font=dict(size=16, family="Outfit, Inter, sans-serif", color="#1e293b"),
        font=dict(family="Inter, sans-serif", color="#475569"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
