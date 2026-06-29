import json
import logging
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

# Configure logging to output to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
        options=[
            "Jadwal Ujian (Utama)",
            "Performa & Konflik",
            "Evolusi Fitness",
            "Cara Kerja GA",
        ],
        icons=["calendar3", "bar-chart-line", "graph-up", "info-circle"],
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

# ==================== MENU 4: CARA KERJA GA ====================
elif menu == "Cara Kerja GA":
    st.title("Cara Kerja Algoritma Genetika (Genetic Algorithm)")
    st.write(
        "Halaman ini menjelaskan alur logika dan cara kerja Genetic Algorithm (GA) "
        "serta Hybrid GA dalam menyelesaikan masalah penjadwalan ujian universitas."
    )

    # 1. Flowchart visual menggunakan Graphviz
    st.write("### Diagram Alur (Flowchart) Algoritma")
    dot = """
    digraph G {
        rankdir=TB;
        node [shape=box, style="filled,rounded", color="#4f46e5", fontcolor=white, fillcolor="#4f46e5", fontname="Inter"];
        edge [color="#64748b", fontname="Inter"];
        
        Start [label="Start: Inisialisasi Populasi\\n(Populasi Awal Acak + Greedy Seed)", fillcolor="#10b981", color="#10b981"];
        Fitness [label="Evaluasi Fitness\\n(Hitung Total Penalti dari 10 Constraints)"];
        Selection [label="Seleksi Turnamen\\n(Pilih Orang Tua Berdasarkan Penalti Terendah)"];
        Crossover [label="Crossover (Kawin Silang)\\n(One-Point atau Uniform Crossover)"];
        Mutation [label="Mutasi (Eksplorasi)\\n(Swap Mutation atau Move Mutation)"];
        Repair [label="Greedy Local Repair\\n(Hanya diaktifkan pada Hybrid GA)", fillcolor="#0ea5e9", color="#0ea5e9"];
        Elitism [label="Elitisme\\n(Salin Solusi Terbaik Langsung ke Generasi Baru)"];
        Check [label="Cek Konvergensi?\\n(Mencapai Batas Generasi Maksimal?)", shape=diamond, fillcolor="#f59e0b", color="#f59e0b"];
        End [label="End: Solusi Jadwal Terbaik\\n(Simpan ke outputs/schedule.csv)", fillcolor="#ef4444", color="#ef4444"];
        
        Start -> Fitness;
        Fitness -> Elitism;
        Fitness -> Selection;
        Selection -> Crossover;
        Crossover -> Mutation;
        Mutation -> Repair;
        Repair -> Check;
        Elitism -> Check;
        Check -> Fitness [label="Tidak"];
        Check -> End [label="Ya"];
    }
    """
    st.graphviz_chart(dot)

    st.write("---")
    st.write("### Penjelasan Tahapan Kerja GA")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "1. Representasi & Populasi",
            "2. Operator Genetika",
            "3. Hibridisasi (Local Repair)",
            "4. Demo Simulasi Interaktif (Dataset Nyata)",
        ]
    )

    with tab1:
        st.markdown(
            """
            #### A. Representasi Kromosom (Chromosome Representation)
            * **Gen (Gene)**: Mewakili satu mata kuliah yang harus dijadwalkan (misal: `KOM401`).
            * **Kromosom (Chromosome)**: Mewakili satu solusi jadwal ujian lengkap. Struktur internal direpresentasikan dalam bentuk larik integer (`list[int]`):
              * Indeks pada list menunjukkan mata kuliah (berdasarkan urutan di `courses.csv`).
              * Nilai di dalam indeks tersebut mewakili ID slot waktu (`slot_id`) ujian yang dialokasikan.
            
            #### B. Inisialisasi Populasi (Population Initialization)
            * **Pure GA**: Membangkitkan sejumlah individu secara acak untuk membentuk populasi awal.
            * **Hybrid GA (Heuristic Seeding)**: Menyertakan solusi dari **Greedy Heuristic** ke dalam populasi awal. Hal ini memberikan titik awal yang terarah, sehingga pencarian berjalan jauh lebih cepat.
            """
        )

    with tab2:
        st.markdown(
            """
            #### A. Evaluasi Fitness (Fitness Evaluation)
            Mengukur kualitas kromosom berdasarkan total penalti. **Nilai penalti yang lebih kecil menunjukkan solusi yang lebih baik (optimal).**
            * **Hard Constraints (HC)**: Batasan wajib. Jika dilanggar, penalti sangat tinggi (`1000` per pelanggaran). Meliputi: bentrok ujian mahasiswa, kapasitas ruangan ujian terlampaui, dan jadwal yang diblokir fakultas.
            * **Soft Constraints (SC)**: Batasan kenyamanan. Memiliki bobot penalti lebih kecil (misal: ujian berturut-turut, tidak ada jeda sesi).
            
            #### B. Seleksi Orang Tua (Selection)
            Menggunakan **Tournament Selection**. Sistem mengambil sejumlah individu acak dari populasi (ukuran turnamen $K=5$) dan memilih individu dengan penalti terendah (terbaik) untuk dijadikan orang tua.
            
            #### C. Kawin Silang (Crossover)
            Menggabungkan gen dari dua orang tua untuk melahirkan anak. Dipilih secara acak antara:
            * **One-Point Crossover**: Memotong gen di satu titik dan menukarnya.
            * **Uniform Crossover**: Setiap gen anak dipilih secara independen dari salah satu orang tua berdasarkan peluang acak.
            
            #### D. Mutasi (Mutation)
            Melakukan perubahan kecil acak pada anak untuk menjaga keberagaman gen dan keluar dari optimum lokal.
            * **Swap Mutation**: Menukar slot waktu ujian dari dua mata kuliah.
            * **Move Mutation**: Memindahkan satu ujian ke slot waktu acak lainnya.
            
            #### E. Elitisme (Elitism)
            Menyalin langsung 2 individu terbaik dari generasi saat ini ke generasi berikutnya untuk menjamin solusi terbaik tidak pernah hilang selama evolusi.
            """
        )

    with tab3:
        st.markdown(
            """
            #### Mengapa Perlu Local Repair (Hybrid GA)?
            Pada masalah penjadwalan yang sangat padat (*highly constrained bottlenecks*), mutasi acak dan crossover dari Pure GA seringkali tidak sengaja merusak jadwal yang sudah rapi (*disruptive effect*). Akibatnya, Pure GA sering terjebak dengan sisa bentrokan hard constraint yang sulit hilang.
            
            #### Cara Kerja Greedy Repair (Memetic Local Search)
            Hybrid GA mengaktifkan fitur Greedy Repair dengan peluang 20% pada keturunan baru:
            1. **Deteksi Bentrok Aktif**: Skrip mendeteksi secara presisi mata kuliah mana saja yang saat ini masih memiliki bentrokan jadwal mahasiswa (*Hard Constraint*).
            2. **Targeted Greedy Search**: Memilih maksimal 3 mata kuliah yang bentrok, lalu mencoba memindahkannya ke setiap slot waktu lain (1 sampai 10) secara sekuensial.
            3. **Simpan Hasil Terbaik**: Jika pemindahan tersebut menurunkan nilai penalti, slot waktu baru tersebut disimpan.
            4. **Nol Overhead**: Ketika jadwal sudah bersih dari bentrokan (fitness stabil), fungsi repair selesai dalam 0 milidetik tanpa membuang siklus CPU.
            """
        )

    with tab4:
        # Track active demo step in session state
        if "demo_step" not in st.session_state:
            st.session_state.demo_step = 1

        st.write(f"### Demo Alur Kerja GA: Langkah {st.session_state.demo_step} dari 7")

        # Navigation buttons at the top of the content
        col_nav_back, col_nav_space, col_nav_next = st.columns([1, 4, 1])
        with col_nav_back:
            if st.session_state.demo_step > 1:
                if st.button("Kembali", key="btn_nav_back"):
                    st.session_state.demo_step -= 1
                    st.rerun()
        with col_nav_next:
            if st.session_state.demo_step < 7:
                if st.button("Lanjut", key="btn_nav_next"):
                    st.session_state.demo_step += 1
                    st.rerun()

        st.write("---")

        # Load dataset
        from src.preprocessing.conflict_matrix import build_conflict_matrix
        from src.preprocessing.load_dataset import load_dataset
        from src.utils.constants import DATA_DIR

        try:
            students, courses, enrollments, timeslots, rooms, slot_blocks = (
                load_dataset(DATA_DIR)
            )
            conflict_matrix = build_conflict_matrix(enrollments, courses)
            course_map = {c.course_id: c for c in courses}

            # Precompute overlap
            from collections import defaultdict

            course_students = defaultdict(set)
            for e in enrollments:
                course_students[e.course_id].add(e.student_id)

            max_overlap = 0
            best_pair = None
            course_ids_list = list(course_students.keys())
            for i in range(len(course_ids_list)):
                for j in range(i + 1, len(course_ids_list)):
                    c1 = course_ids_list[i]
                    c2 = course_ids_list[j]
                    overlap = len(course_students[c1].intersection(course_students[c2]))
                    if overlap > max_overlap:
                        max_overlap = overlap
                        best_pair = (c1, c2)

            c1, c2 = best_pair if best_pair else ("KOM401", "KOM402")
            c1_name = (
                course_map[c1].course_name if c1 in course_map else "Pemrograman Dasar"
            )
            c2_name = (
                course_map[c2].course_name if c2 in course_map else "Struktur Data"
            )
            common_students = (
                sorted(list(course_students[c1].intersection(course_students[c2])))
                if best_pair
                else []
            )

            # Step 1: Memuat Dataset
            if st.session_state.demo_step == 1:
                st.markdown(
                    f"""
                    #### Langkah 1: Memuat Dataset Ujian (Input File)
                    Sistem pertama kali memuat semua berkas data dari folder `data/` untuk mendeteksi relasi penjadwalan.
                    
                    **Ringkasan Data Terbaca dari Dataset Aktif:**
                    * Total Mahasiswa: {len(students)} orang
                    * Total Mata Kuliah: {len(courses)} mata kuliah
                    * Total KRS/Koneksi Pendaftaran: {len(enrollments)} krs
                    * Total Slot Waktu Tersedia: {len(timeslots)} slot
                    * Total Ruangan Ujian: {len(rooms)} ruangan
                    
                    *Penjelasan*: Langkah awal ini sangat penting untuk memastikan tidak ada ID mata kuliah atau mahasiswa yang tidak terdaftar atau bermasalah pada dataset sebelum algoritma dijalankan.
                    """
                )
                import pandas as pd

                st.write("Preview 5 Baris Data Mata Kuliah (courses.csv):")
                df_c_preview = pd.DataFrame(
                    [
                        {
                            "ID": c.course_id,
                            "Nama": c.course_name,
                            "Dosen": c.lecturer_id,
                        }
                        for c in courses[:5]
                    ]
                )
                st.dataframe(df_c_preview, use_container_width=True, hide_index=True)

            # Step 2: Membangun Matriks Konflik
            elif st.session_state.demo_step == 2:
                st.markdown(
                    f"""
                    #### Langkah 2: Membangun Matriks Konflik (Conflict Matrix)
                    Setelah data dimuat, sistem mendeteksi relasi bentrokan mata kuliah. Jika ada mahasiswa yang mengambil dua mata kuliah sekaligus, kedua mata kuliah tersebut didefinisikan saling konflik (tidak boleh ditaruh di slot sesi yang sama).
                    
                    **Hasil Analisis Konflik pada Data Aktif:**
                    * Total pasangan mata kuliah yang berkonflik: {sum(len(v) for v in conflict_matrix.values()) // 2} pasangan.
                    * Contoh konflik terbesar terdeteksi antara:
                      * `{c1}` ({c1_name}) dan `{c2}` ({c2_name}).
                      * Sebanyak **{max_overlap} mahasiswa** mengambil kedua kelas ini bersamaan.
                    """
                )
                st.write("Daftar ID Mahasiswa yang Terkena Bentrokan:")
                st.write(
                    ", ".join(common_students[:40])
                    + ("..." if len(common_students) > 40 else "")
                )

            # Step 3: Inisialisasi Populasi Awal
            elif st.session_state.demo_step == 3:
                st.markdown(
                    """
                    #### Langkah 3: Inisialisasi Populasi Awal (Greedy Seeding)
                    Algoritma membuat populasi awal sebanyak 50 kandidat jadwal. 
                    * Pada **Pure GA**, semua jadwal diisi secara acak sehingga penaltinya sangat besar.
                    * Pada **Hybrid GA**, sistem membuat satu jadwal pembuka menggunakan **Greedy Baseline Solver** (penjadwalan sekuensial berdasarkan prioritas tingkat konflik terbesar), lalu menyisipkannya sebagai seed/benih di populasi agar evolusi memiliki titik awal yang terarah (tidak acak murni).
                    """
                )
                # Show mock chromosome mapping
                st.write(
                    "Simulasi Kode Genetik Kromosom Awal (Mata Kuliah -> Slot Waktu):"
                )
                import pandas as pd

                sample_genes = []
                for idx, c in enumerate(courses[:6]):
                    sample_genes.append(
                        {
                            "Mata Kuliah": c.course_id,
                            "Nama Mata Kuliah": c.course_name,
                            "Slot Sesi Terpilih": f"Slot {idx + 1}",
                        }
                    )
                st.table(pd.DataFrame(sample_genes))

            # Step 4: Evaluasi Fitness (Menghitung Pelanggaran & Penalti)
            elif st.session_state.demo_step == 4:
                st.markdown(
                    f"""
                    #### Langkah 4: Evaluasi Fitness (Menghitung Pinalti)
                    Setiap individu dinilai menggunakan fungsi fitness. Penalti ditambahkan jika ada pelanggaran batasan:
                    * **Hard Constraints (HC)**: Batasan wajib. Penalti +1000 per pelanggaran (bentrokan jadwal mahasiswa, kapasitas ruangan terlampaui, slot diblokir).
                    * **Soft Constraints (SC)**: Batasan kenyamanan. Penalti kecil (ujian beruntun di hari yang sama, tidak ada jeda sesi).
                    
                    **Contoh Skenario Pelanggaran Hard Constraint:**
                    Jika sistem menjadwalkan `{c1}` dan `{c2}` secara bersamaan di Slot 1, sistem akan mencatat pelanggaran bentrokan jadwal:
                    """
                )
                penalty_val = max_overlap * 1000
                st.error(
                    f"Pelanggaran Hard Constraint Terdeteksi: {max_overlap} mahasiswa bentrok jadwal ujian!\n"
                    f"Perhitungan Penalti: {max_overlap} mahasiswa dikali 1000 = **{penalty_val}** poin penalti."
                )

            # Step 5: Operator Crossover & Mutasi (Evolusi)
            elif st.session_state.demo_step == 5:
                st.markdown(
                    """
                    #### Langkah 5: Operator Genetika (Crossover & Mutasi)
                    Untuk mengeksplorasi susunan jadwal baru yang lebih optimal secara global, sistem mengambil sepasang orang tua terbaik dan menerapkan:
                    1. **Crossover (Kawin Silang)**: Menukar slot waktu ujian antar mata kuliah dari dua orang tua untuk melahirkan anak.
                    2. **Mutasi**: Memindahkan slot waktu mata kuliah secara acak (Move Mutation) atau menukar slot waktu antara dua mata kuliah (Swap Mutation) dengan probabilitas Mutation Rate.
                    """
                )
                st.write("Simulasi Pertukaran Genetik Crossover:")
                col_p1, col_p2, col_ch = st.columns(3)
                with col_p1:
                    st.info(
                        "Orang Tua 1 (Jadwal A)\n\nKOM401 -> Slot 1\nKOM402 -> Slot 1\nKOM403 -> Slot 2"
                    )
                with col_p2:
                    st.info(
                        "Orang Tua 2 (Jadwal B)\n\nKOM401 -> Slot 3\nKOM402 -> Slot 2\nKOM403 -> Slot 2"
                    )
                with col_ch:
                    st.success(
                        "Anak Hasil Crossover\n\nKOM401 -> Slot 1 (dari Ortu 1)\nKOM402 -> Slot 2 (dari Ortu 2)\nKOM403 -> Slot 2 (dari Ortu 1/2)"
                    )

            # Step 6: Operator Perbaikan Lokal (Greedy Repair)
            elif st.session_state.demo_step == 6:
                st.markdown(
                    f"""
                    #### Langkah 6: Operator Perbaikan Lokal (Greedy Local Repair)
                    Pada Hybrid GA, keturunan baru yang dihasilkan oleh mutasi/crossover diperiksa konflik hard-nya. Jika ada konflik (seperti bentrokan mahasiswa `{c1}` dan `{c2}` di Slot 1), Greedy Repair mengunci `{c1}` di Slot 1, lalu mencoba memindahkan `{c2}` ke slot alternatif lainnya untuk mencari penalti minimum:
                    """
                )
                test_results = []
                for slot in sorted([t.slot_id for t in timeslots]):
                    clashes = max_overlap if slot == 1 else 0
                    penalty = clashes * 1000
                    status = (
                        "Bentrok (Tidak Layak)"
                        if slot == 1
                        else "Bebas Konflik (Layak)"
                    )

                    test_results.append(
                        {
                            "Slot ID": slot,
                            "Hari": f"Hari {next(t.day for t in timeslots if t.slot_id == slot)}",
                            "Sesi": f"Sesi {next(t.session for t in timeslots if t.slot_id == slot)}",
                            "Mahasiswa Bentrok": clashes,
                            "Penalti Hard Constraint": penalty,
                            "Kelayakan Sesi": status,
                        }
                    )
                st.table(test_results)
                st.success(
                    f"Hasil Perbaikan: Mata kuliah `{c2}` dipindahkan dari Slot 1 ke Slot 2.\n"
                    f"Dampak: Penalti bentrokan berhasil diturunkan dari **{max_overlap * 1000}** menjadi **0**."
                )

            # Step 7: Konvergensi dan Hasil Akhir (Output)
            elif st.session_state.demo_step == 7:
                st.markdown(
                    """
                    #### Langkah 7: Konvergensi dan Penyimpanan Hasil Akhir (Output)
                    Sistem terus mengulangi proses evaluasi, crossover, mutasi, dan perbaikan lokal hingga mencapai generasi maksimal (generasi 50).
                    
                    Solusi terbaik yang memiliki nilai penalti terendah (biasanya bernilai 0 untuk pelanggaran Hard Constraint) akan dipilih sebagai jadwal resmi dan diekspor ke dalam berkas **`outputs/schedule.csv`**.
                    
                    Jadwal hasil optimasi ini dapat dicari, difilter berdasarkan hari dan sesi, serta diunduh di tab utama **Jadwal Ujian (Utama)**.
                    """
                )
                import pandas as pd

                st.write("Preview Format Berkas Jadwal Akhir (outputs/schedule.csv):")
                df_out_preview = pd.DataFrame(
                    [
                        {
                            "course_id": c.course_id,
                            "course_name": c.course_name,
                            "slot_id": idx + 1,
                            "day": (idx // 3) + 1,
                            "session": (idx % 3) + 1,
                        }
                        for idx, c in enumerate(courses[:5])
                    ]
                )
                st.dataframe(df_out_preview, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Gagal memuat visualisasi simulasi alur kerja: {e}")
