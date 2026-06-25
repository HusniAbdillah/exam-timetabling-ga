# Exam Timetabling using Genetic Algorithm

Implementasi **Genetic Algorithm (GA)** untuk menyelesaikan permasalahan **University Exam Timetabling Problem (UETP)** sebagai tugas mata kuliah **Pengantar Kecerdasan Komputasional**.

## Deskripsi

Proyek ini bertujuan membangun sistem optimasi penjadwalan ujian pada sebuah universitas yang terdiri atas beberapa fakultas, program studi, dan mata kuliah. Fokus penelitian adalah menentukan penempatan setiap ujian ke dalam slot waktu sehingga konflik antar mahasiswa dapat diminimalkan.

Model yang digunakan merupakan penyederhanaan dari University Exam Timetabling Problem dengan ruang lingkup optimasi hanya pada **penempatan ujian ke slot waktu (Exam → Timeslot)**. Penjadwalan ruang ujian, pengawas, maupun kapasitas ruang tidak termasuk dalam cakupan penelitian agar implementasi tetap berfokus pada Genetic Algorithm.

Dataset yang digunakan merupakan dataset simulasi yang merepresentasikan struktur universitas dengan banyak program studi, mata kuliah umum, dan mata kuliah program studi sehingga menghasilkan conflict graph yang menyerupai kondisi nyata.

---

## Tujuan

* Mengimplementasikan Genetic Algorithm pada permasalahan optimasi penjadwalan ujian.
* Menghasilkan jadwal ujian dengan jumlah konflik mahasiswa seminimal mungkin.
* Membandingkan hasil Genetic Algorithm dengan algoritma Greedy sebagai baseline.
* Menyediakan aplikasi demonstrasi sederhana untuk memvisualisasikan proses optimasi.

---

## Ruang Lingkup

### Termasuk

* Simulasi data universitas.
* Preprocessing dataset.
* Pembentukan conflict matrix.
* Implementasi Genetic Algorithm.
* Evaluasi hasil.
* Visualisasi jadwal dan perkembangan fitness.

### Tidak Termasuk

* Penjadwalan ruang ujian.
* Penjadwalan pengawas.
* Optimasi kapasitas ruang.
* Sistem informasi akademik.
* Manajemen pengguna.
* Database.
* REST API.

---

## Struktur Repository

```text
exam-timetabling-ga
│
├── app/
├── data/
├── development/
│   ├── standards/
│   │   ├── CODING_STANDARD.md
│   │   ├── DATA_SPEC.md
│   │   └── TYPE_GUIDELINES.md
│   ├── GIT_WORKFLOW.md
│   ├── TEAM_TASKS.md
│   └── UV_SETUP.md
├── docs/
├── outputs/
├── src/
│   └── models/
├── tests/
│
├── README.md
├── PRD.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── pyproject.toml
└── uv.lock
```

---

## Teknologi

| Komponen            | Teknologi     |
| ------------------- | ------------- |
| Bahasa Pemrograman  | Python 3.11+  |
| Environment Manager | uv            |
| User Interface      | Streamlit     |
| Data Processing     | Pandas, NumPy |
| Visualisasi         | Plotly        |
| Testing             | pytest        |
| Linting             | Ruff          |

---

## Dataset

Dataset disimpan pada direktori `data/` dan terdiri atas beberapa berkas CSV.

```text
data/
├── students.csv
├── courses.csv
├── enrollment.csv
└── timeslots.csv
```

Seluruh dataset dibaca secara lokal oleh aplikasi. Tidak terdapat mekanisme upload dataset pada antarmuka pengguna.

---

## Menjalankan Proyek

### 1. Clone Repository

```bash
git clone <repository-url>
cd exam-timetabling-ga
```

### 2. Sinkronisasi Environment

```bash
uv sync
```

### 3. Menjalankan Aplikasi

```bash
uv run streamlit run app/app.py
```

---

## Output

Aplikasi menghasilkan beberapa keluaran berikut.

* Jadwal ujian terbaik.
* Nilai fitness terbaik.
* Grafik perkembangan fitness setiap generasi.
* Statistik konflik mahasiswa.
* Perbandingan Genetic Algorithm dan Greedy.

Seluruh hasil eksperimen disimpan pada direktori `outputs/`.

---

## Tim Pengembang

| Peran                      | Tanggung Jawab                                   |
| -------------------------- | ------------------------------------------------ |
| Project Lead               | Koordinasi proyek, integrasi sistem, dokumentasi |
| Dataset & Preprocessing    | Dataset, preprocessing, conflict matrix          |
| Genetic Algorithm          | Implementasi Genetic Algorithm                   |
| Fitness & Constraint       | Evaluasi fitness dan constraint                  |
| Evaluation & Visualization | Baseline, evaluasi, visualisasi                  |

---

## Mata Kuliah

Pengantar Kecerdasan Komputasional

Topik:

**Evolutionary Computation — Genetic Algorithm**

---

## Lisensi

Repository ini dikembangkan untuk keperluan akademik sebagai tugas mata kuliah Pengantar Kecerdasan Komputasional.
