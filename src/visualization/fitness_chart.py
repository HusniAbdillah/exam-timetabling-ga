from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_fitness_chart(
    history_df_or_path: pd.DataFrame | Path | str,
) -> go.Figure:
    """Membuat grafik garis interaktif untuk visualisasi penurunan penalti
    (fitness) per generasi.

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

    # Buat grafik garis
    fig = px.line(
        df,
        x="generation",
        y="best_fitness",
        labels={"generation": "Generasi", "best_fitness": "Fitness (Total Penalti)"},
        template="plotly_white",
    )

    # Mempercantik tampilan grafik agar terlihat premium
    fig.update_traces(
        line=dict(color="#4f46e5", width=3),  # Indigo accent
        mode="lines",
        hovertemplate="Generasi: %{x}<br>Fitness: %{y}<extra></extra>",
    )

    fig.update_layout(
        hovermode="x unified",
        margin=dict(l=40, r=40, t=20, b=40),
        font=dict(family="Inter, sans-serif", color="#475569"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            zeroline=False,
            title_font=dict(size=14),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            zeroline=False,
            title_font=dict(size=14),
            title_text="Fitness (Lebih Rendah Lebih Baik)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig
