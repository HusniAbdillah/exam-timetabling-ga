from pathlib import Path

import pandas as pd


def build_schedule_table(
    schedule_df_or_path: pd.DataFrame | Path | str,
) -> pd.DataFrame:
    """Membaca dan memformat DataFrame jadwal ujian untuk ditampilkan di dashboard.

    Args:
        schedule_df_or_path: DataFrame atau path file ke berkas schedule.csv.

    Returns:
        pd.DataFrame: DataFrame terformat yang siap ditampilkan,
            diurutkan berdasarkan Hari dan Sesi.
    """
    if isinstance(schedule_df_or_path, (str, Path)):
        df = pd.read_csv(schedule_df_or_path)
    else:
        df = schedule_df_or_path.copy()

    # Hari -> Sesi -> Kode Mata Kuliah
    df = df.sort_values(by=["day", "session", "course_id"])

    df_formatted = df.rename(
        columns={
            "course_id": "Kode Matakuliah",
            "course_name": "Nama Matakuliah",
            "slot_id": "ID Slot",
            "day": "Hari",
            "session": "Sesi",
        }
    )

    cols = ["Kode Matakuliah", "Nama Matakuliah", "ID Slot", "Hari", "Sesi"]
    df_formatted = df_formatted[cols]

    return df_formatted
