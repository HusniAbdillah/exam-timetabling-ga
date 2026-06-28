from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


def plot_fitness_chart(
    history_df_or_path: pd.DataFrame | Path | str,
) -> go.Figure:
    """Membuat grafik garis interaktif untuk visualisasi penurunan penalti
    (fitness) per generasi untuk Pure GA dan Hybrid GA.

    Args:
        history_df_or_path: DataFrame atau path file ke riwayat fitness.

    Returns:
        go.Figure: Objek grafik Plotly.
    """
    if isinstance(history_df_or_path, (str, Path)):
        df = pd.read_csv(history_df_or_path)
    else:
        df = history_df_or_path

    # Urutkan berdasarkan generasi
    df = df.sort_values("generation")

    fig = go.Figure()

    # Trace 1: Pure GA
    if "pure_ga_fitness" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["generation"],
                y=df["pure_ga_fitness"],
                name="Pure GA",
                mode="lines",
                line=dict(color="#0ea5e9", width=3),
                hovertemplate="Generasi: %{x}<br>Pure GA: %{y}<extra></extra>",
            )
        )
    elif "best_fitness" in df.columns:
        # Fallback untuk data lama
        fig.add_trace(
            go.Scatter(
                x=df["generation"],
                y=df["best_fitness"],
                name="Pure GA",
                mode="lines",
                line=dict(color="#0ea5e9", width=3),
                hovertemplate="Generasi: %{x}<br>Pure GA: %{y}<extra></extra>",
            )
        )

    # Trace 2: Hybrid GA
    if "hybrid_ga_fitness" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["generation"],
                y=df["hybrid_ga_fitness"],
                name="Hybrid GA (Greedy + GA)",
                mode="lines",
                line=dict(color="#4f46e5", width=3),
                hovertemplate="Generasi: %{x}<br>Hybrid GA: %{y}<extra></extra>",
            )
        )

    fig.update_layout(
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=40),
        font=dict(family="Inter, sans-serif", color="#475569"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            zeroline=False,
            title_text="Generasi",
            title_font=dict(size=14),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            zeroline=False,
            title_font=dict(size=14),
            title_text="Fitness (Total Penalti)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig
