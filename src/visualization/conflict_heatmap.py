from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def build_conflict_matrix_data(
    enrollments_file: Path,
    courses_file: Path,
) -> tuple[list[str], np.ndarray]:
    """Build a quantitative conflict matrix from enrollment records.

    Calculates the count of students sharing both courses for every pair.

    Args:
        enrollments_file: Path to enrollment.csv.
        courses_file: Path to courses.csv.

    Returns:
        tuple: (list of course_ids, 2D numpy array of conflict counts).
    """
    df_enroll = pd.read_csv(enrollments_file)
    df_courses = pd.read_csv(courses_file)

    course_ids = sorted(df_courses["course_id"].tolist())
    n = len(course_ids)

    matrix = np.zeros((n, n), dtype=int)
    course_idx = {c: i for i, c in enumerate(course_ids)}

    # Group by student
    student_courses = df_enroll.groupby("student_id")["course_id"].apply(list)

    for courses in student_courses:
        for i in range(len(courses)):
            for j in range(len(courses)):
                c1 = courses[i]
                c2 = courses[j]
                if c1 in course_idx and c2 in course_idx:
                    matrix[course_idx[c1], course_idx[c2]] += 1

    return course_ids, matrix


def plot_conflict_heatmap(enrollments_file: Path, courses_file: Path) -> go.Figure:
    """Plot the university conflict matrix as an interactive Plotly Heatmap.

    Args:
        enrollments_file: Path to enrollment.csv.
        courses_file: Path to courses.csv.

    Returns:
        go.Figure: Interactive Heatmap figure.
    """
    course_ids, matrix = build_conflict_matrix_data(enrollments_file, courses_file)

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=course_ids,
            y=course_ids,
            colorscale="Plasma",
            colorbar=dict(title="Siswa Bentrok"),
            hovertemplate=(
                "Matkul X: %{x}<br>"
                "Matkul Y: %{y}<br>"
                "Siswa Bentrok: %{z}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis=dict(tickangle=-90, title="Kode Mata Kuliah", showgrid=False),
        yaxis=dict(title="Kode Mata Kuliah", showgrid=False),
        margin=dict(l=60, r=40, t=20, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig
