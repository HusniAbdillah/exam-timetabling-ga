import json
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu

from src.config.app_config import APP_ICON, APP_TITLE
from src.utils.constants import COURSES_CSV, ENROLLMENTS_CSV
from src.visualization.conflict_heatmap import plot_conflict_heatmap
from src.visualization.fitness_chart import plot_fitness_chart
from src.visualization.schedule_table import build_schedule_table
from src.visualization.statistics import (
    plot_fitness_comparison,
    plot_violations_comparison,
)

# Configuration for Streamlit Page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Premium CSS Styling
css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Project Paths
PROJECT_ROOT = Path(__file__).parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"
schedule_file = OUTPUT_DIR / "schedule.csv"
fitness_file = OUTPUT_DIR / "fitness_history.csv"
stats_file = OUTPUT_DIR / "statistics.json"

# Initialize Session State
if "optimization_run" not in st.session_state:
    st.session_state.optimization_run = False


def run_actual_optimization(pop_size, max_gens, crossover_rate, mutation_rate):
    """Run optimization with chosen hyperparameters."""
    from src.evaluation.benchmark import run_benchmark
    from src.ga.engine import GAConfig

    config = GAConfig(
        population_size=pop_size,
        max_generations=max_gens,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
    )

    run_benchmark(config)
    st.session_state.optimization_run = True


# Sidebar Configuration
with st.sidebar:
    st.markdown("### Menu Navigasi")
    menu = option_menu(
        menu_title=None,
        options=["Jadwal Ujian (Utama)", "Performa & Konflik", "Evolusi Fitness"],
        icons=["calendar3", "bar-chart-line", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"font-size": "16px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#4f46e5", "color": "white"},
        },
    )

    st.markdown("---")
    st.markdown("### Parameter GA")
    pop_size = st.slider(
        "Ukuran Populasi (Population Size)",
        min_value=10,
        max_value=150,
        value=50,
        step=10,
    )
    max_gens = st.slider(
        "Jumlah Generasi (Max Generations)",
        min_value=10,
        max_value=150,
        value=50,
        step=10,
    )
    crossover_rate = st.slider(
        "Crossover Rate",
        min_value=0.1,
        max_value=1.0,
        value=0.8,
        step=0.05,
    )
    mutation_rate = st.slider(
        "Mutation Rate",
        min_value=0.01,
        max_value=0.5,
        value=0.1,
        step=0.01,
    )

st.sidebar.markdown("---")
st.sidebar.info("Pengantar Kecerdasan Komputasional - Kelompok 17")


# ==================== MENU 1: JADWAL UJIAN (UTAMA) ====================
if menu == "Jadwal Ujian (Utama)":
    st.title("Dashboard Penjadwalan Ujian Universitas")
    st.subheader("Optimasi Penjadwalan Ujian Menggunakan Genetic Algorithm")

    col_btn, col_info = st.columns([1, 4], gap="small")
    with col_btn:
        btn_click = st.button(
            "Mulai Optimasi Jadwal",
            help="Jalankan untuk generate jadwal yang minimal konflik",
        )
    with col_info:
        st.markdown(
            "<p style='color: #64748b; font-size: 14px; "
            "margin-top: 8px; margin-left: -25px;'>"
            "Jalankan untuk generate jadwal yang minimal konflik"
            "</p>",
            unsafe_allow_html=True,
        )

    placeholder = st.empty()

    if btn_click:
        with placeholder.container():
            with st.spinner("Menjalankan optimasi penjadwalan ujian..."):
                run_actual_optimization(
                    pop_size, max_gens, crossover_rate, mutation_rate
                )

    if st.session_state.optimization_run or schedule_file.exists():
        if schedule_file.exists():
            st.success("Jadwal Ujian Terbaik Berhasil Dibuat!")

            # Load schedule data
            df_schedule = build_schedule_table(schedule_file)

            st.write("### Filter dan Pencarian Jadwal")
            col_f1, col_f2, col_f3 = st.columns(3)

            with col_f1:
                search_query = st.text_input(
                    "Cari Nama/Kode Matakuliah:", placeholder="Ketik di sini..."
                )
            with col_f2:
                days_list = ["Semua Hari"] + sorted(
                    df_schedule["Hari"].unique().tolist()
                )
                filter_day = st.selectbox("Filter berdasarkan Hari:", days_list)
            with col_f3:
                sessions_list = ["Semua Sesi"] + sorted(
                    df_schedule["Sesi"].unique().tolist()
                )
                filter_session = st.selectbox("Filter berdasarkan Sesi:", sessions_list)

            # Apply filters
            df_filtered = df_schedule.copy()
            if search_query:
                df_filtered = df_filtered[
                    df_filtered["Nama Matakuliah"].str.contains(
                        search_query, case=False
                    )
                    | df_filtered["Kode Matakuliah"].str.contains(
                        search_query, case=False
                    )
                ]
            if filter_day != "Semua Hari":
                df_filtered = df_filtered[df_filtered["Hari"] == filter_day]
            if filter_session != "Semua Sesi":
                df_filtered = df_filtered[df_filtered["Sesi"] == filter_session]

            col_tbl_header, col_download = st.columns([3, 1])
            with col_tbl_header:
                st.write(f"Menampilkan {len(df_filtered)} mata kuliah terjadwal:")
            with col_download:
                try:
                    with open(schedule_file, encoding="utf-8") as f:
                        csv_data = f.read()
                    st.download_button(
                        label="Unduh Jadwal (CSV)",
                        data=csv_data,
                        file_name="jadwal_ujian_teroptimasi.csv",
                        mime="text/csv",
                    )
                except Exception:
                    pass

            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        else:
            st.warning("Berkas jadwal tidak ditemukan di direktori outputs.")
    else:
        st.write("---")
        st.info(
            "Jadwal belum dioptimasi. Harap tekan tombol Mulai Optimasi Jadwal di atas."
        )

# ==================== MENU 2: PERFORMA & KONFLIK ====================
elif menu == "Performa & Konflik":
    st.title("Metrik Performa & Statistik Konflik")
    st.write(
        "Halaman ini membandingkan hasil optimasi antara "
        "Genetic Algorithm (GA) dengan algoritma Greedy baseline."
    )

    if stats_file.exists():
        with open(stats_file, encoding="utf-8") as f:
            stats = json.load(f)

        # Backwards compatibility check
        pure_ga_data = stats.get("pure_ga", stats.get("ga", {}))
        greedy_data = stats.get("greedy", {})
        hybrid_ga_data = stats.get("hybrid_ga", pure_ga_data)

        pure_ga_fit = pure_ga_data.get("best_fitness", 0.0)
        greedy_fit = greedy_data.get("best_fitness", 0.0)
        hybrid_ga_fit = hybrid_ga_data.get("best_fitness", 0.0)

        st.write("### Perbandingan Performa")
        col_m1, col_m2, col_m3 = st.columns(3)

        with col_m1:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: #0ea5e9;">
                    <p class="metric-title">Pure GA Best Fitness</p>
                    <p class="metric-value">{pure_ga_fit:.1f}</p>
                    <span class="metric-badge badge-sky">Eksplorasi Stokastik Murni</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_m2:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: #64748b;">
                    <p class="metric-title">Greedy Baseline Fitness</p>
                    <p class="metric-value">{greedy_fit:.1f}</p>
                    <span class="metric-badge badge-error">Heuristik Sekuensial Terbatas</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_m3:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: #4f46e5;">
                    <p class="metric-title">Hybrid GA Best Fitness</p>
                    <p class="metric-value">{hybrid_ga_fit:.1f}</p>
                    <span class="metric-badge badge-ok">Heuristic Seeding Optimal</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        improvement = 0.0
        if greedy_fit > 0:
            improvement = ((greedy_fit - hybrid_ga_fit) / greedy_fit) * 100
        if improvement > 0:
            st.success(
                f"Analisis Sukses: Inisialisasi Hybrid (Heuristic Seeding) berhasil meningkatkan "
                f"kualitas solusi penjadwalan sebesar **{improvement:.1f}%** dibandingkan Greedy Baseline."
            )

        st.write("---")
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            st.markdown("##### Perbandingan Kualitas Solusi (Lebih Rendah Lebih Baik)")
            st.plotly_chart(
                plot_fitness_comparison(stats_file), use_container_width=True
            )
        with col_c2:
            st.markdown("##### Perbandingan Detail Pelanggaran & Penalti")
            st.plotly_chart(
                plot_violations_comparison(stats_file), use_container_width=True
            )

        st.write("---")
        st.markdown("##### Analisis Matriks Konflik (Conflict Matrix)")
        st.plotly_chart(
            plot_conflict_heatmap(ENROLLMENTS_CSV, COURSES_CSV),
            use_container_width=True,
        )

        st.write("---")
        st.write("### Rincian Detail Pelanggaran Batasan (Violations)")
        col_detail_pure, col_detail_greedy, col_detail_hybrid = st.columns(3)

        with col_detail_pure:
            st.markdown("#### Pure Genetic Algorithm")
            st.json(pure_ga_data)
        with col_detail_greedy:
            st.markdown("#### Greedy Baseline")
            st.json(greedy_data)
        with col_detail_hybrid:
            st.markdown("#### Hybrid Genetic Algorithm")
            st.json(hybrid_ga_data)

    else:
        st.warning(
            "Berkas statistik perbandingan tidak ditemukan di direktori outputs."
        )

# ==================== MENU 3: EVOLUSI FITNESS ====================
elif menu == "Evolusi Fitness":
    st.title("Grafik Evolusi Fitness (Genetic Algorithm)")
    st.write(
        "Halaman ini menampilkan tren penurunan nilai penalti (fitness) "
        "yang dihasilkan oleh populasi terbaik dari setiap generasi."
    )

    if fitness_file.exists():
        st.markdown("##### Perkembangan Nilai Fitness (Total Penalti) per Generasi")
        st.plotly_chart(plot_fitness_chart(fitness_file), use_container_width=True)

        st.write("### Tentang Proses Evolusi GA")
        st.markdown(
            """
            * **Generasi Awal (0-20)**: Nilai penalti turun sangat tajam
              (exploration). Hal ini karena operator mutasi dan crossover
              dengan cepat memperbaiki bentrokan hard constraint dasar.
            * **Generasi Pertengahan (20-70)**: Penurunan penalti mulai melambat.
              Algoritma fokus pada pencarian detail (penjadwalan soft constraint
              seperti menghindari ujian beruntun di hari yang sama).
            * **Generasi Akhir (70+)**: Kurva mendatar (convergence),
              menandakan algoritma telah menemukan solusi optimal lokal/global
              terbaik yang stabil.
            """
        )
    else:
        st.warning("Berkas riwayat fitness tidak ditemukan di direktori outputs.")
