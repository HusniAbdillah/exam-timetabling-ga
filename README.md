# Exam Timetabling using Genetic Algorithm

Implementasi **Genetic Algorithm (GA)** untuk menyelesaikan permasalahan **University Exam Timetabling Problem (UETP)**.

<div align="center">
  
  [![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
  [![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
  [![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
  [![NumPy](https://img.shields.io/badge/NumPy-1.26+-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org)
  [![Pytest](https://img.shields.io/badge/Pytest-8.2+-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org)
  [![Ruff](https://img.shields.io/badge/Ruff-0.4+-ECEFF4?style=flat-square&logo=ruff&logoColor=white)](https://astral.sh/ruff)
  [![License](https://img.shields.io/badge/Lisensi-MIT-green?style=flat-square)](LICENSE)

  Repositori ini dapat diakses di [github.com/HusniAbdillah/exam-timetabling-ga](https://github.com/HusniAbdillah/exam-timetabling-ga)

  > Dikembangkan untuk memenuhi tugas mata kuliah **Pengantar Kecerdasan Komputasional** - Kelompok 17
</div>

---

## Deskripsi

Proyek ini membangun sistem optimasi penjadwalan ujian pada sebuah universitas yang terdiri atas beberapa fakultas, program studi, dan mata kuliah. Fokus utama adalah menentukan penempatan setiap ujian ke dalam slot waktu (timeslot) sedemikian rupa sehingga konflik bentrokan jadwal mahasiswa dapat diminimalkan (Hard Constraint), alokasi kapasitas ruang ujian statis (`rooms.csv`) terpenuhi, serta batasan pemblokiran jadwal fakultas (`slot_blocks.csv`) dipatuhi. Sistem ini juga mengoptimalkan penyebaran ujian mahasiswa lewat serangkaian Soft Constraints.

Optimasi dilakukan menggunakan pendekatan Genetic Algorithm (Pure GA dan Hybrid GA dengan memetic repair mechanism) yang kemudian dibandingkan dengan Greedy baseline.

---

## Alur Eksekusi Sistem (Workflow)

```text
1. Sinkronisasi Dependensi (uv sync)
                │
                ▼
2. Generator Dataset (generate_dataset.py) -> Membuat data/
                │
                ▼
3. Unit Testing & Linter (pytest & ruff) -> Opsional
                │
                ▼
4. Menjalankan Dashboard (run.py) -> Streamlit App
                │
                ▼
5. Melakukan Optimasi & Ekspor Hasil -> outputs/
```

---

## Panduan Perintah Eksekusi (Command References)

Gunakan manajer paket `uv` untuk memastikan konsistensi pustaka yang terpasang di virtual environment.

### 1. Kloning Repository dan Masuk Direktori
```bash
git clone https://github.com/HusniAbdillah/exam-timetabling-ga.git
cd exam-timetabling-ga
```

### 2. Sinkronisasi Dependensi
Unduh dan pasang semua dependensi secara otomatis ke folder `.venv`:
```bash
uv sync
```

### 3. Membangkitkan Dataset Simulasi
Sebelum menjalankan aplikasi, Anda harus membangkitkan data simulasi universitas terlebih dahulu. Data ini meliputi file mahasiswa, kelas, jadwal dasar, pendaftaran, ruangan, dan blokir sesi:
```bash
uv run python scripts/generate_dataset.py
```
*Hasil keluaran disimpan di folder `data/` (`students.csv`, `courses.csv`, `enrollment.csv`, `timeslots.csv`, `rooms.csv`, `slot_blocks.csv`).*

### 4. Menjalankan Unit Test
Verifikasi keselarasan logika mutasi, crossover, conflict matrix, dan perhitungan fitness:
```bash
uv run pytest
```

### 5. Memeriksa Linter dan Formatting
Format ulang gaya penulisan kode sesuai PEP8 serta cek kesalahan sintaks:
```bash
uv run ruff format .
uv run ruff check .
```

### 6. Menjalankan Dashboard Streamlit
Gunakan skrip pembuka terpadu yang dapat dihentikan bersih dengan menekan `Ctrl+C`:
```bash
uv run python run.py
```
*(Alternatif perintah langsung: `uv run streamlit run app/app.py`)*

### 7. Menjalankan Eksperimen Akademik
Untuk menghasilkan data analisis sensitivitas parameter (populasi & mutasi), uji signifikansi statistik (30 runs independen), dan profil kompleksitas waktu secara otomatis:
```bash
uv run python scripts/academic_experiment.py
```
*Hasil analisis disimpan di folder `outputs/` (`sensitivity_analysis.csv`, `sensitivity_analysis.png`, `statistical_significance.json`, `statistical_significance.png`, `time_complexity_profile.json`).*

---

## Panduan Interaksi Antarmuka Streamlit

Aplikasi terbagi menjadi tiga halaman utama yang dapat diakses di sidebar kiri:

### A. Jadwal Ujian (Utama)
1. **Penyetelan Parameter (Sidebar):** Sebelum memulai optimasi, Anda dapat menyetel nilai parameter genetika di panel kiri:
   * **Population Size:** Jumlah individu dalam populasi (rekomendasi: 50-100).
   * **Max Generations:** Batas generasi perulangan evolusi (rekomendasi: 50-100).
   * **Crossover & Mutation Rate:** Probabilitas operator kawin silang dan mutasi gen.
2. **Menjalankan Optimasi:** Tekan tombol **Mulai Optimasi Jadwal** di bagian tengah atas. Sistem akan menjalankan komparasi Genetic Algorithm versus Greedy secara nyata.
3. **Filter & Pencarian:** Setelah jadwal terbentuk, Anda dapat mencari jadwal mata kuliah tertentu dengan mengetik kode/nama mata kuliah, atau melakukan filter berdasarkan hari dan sesi tertentu.
4. **Unduh Berkas:** Tekan tombol **Unduh Jadwal (CSV)** yang muncul di atas tabel untuk mengunduh hasil penjadwalan terbaik ke komputer lokal Anda.

### B. Performa & Konflik
Halaman ini membandingkan kinerja akhir penalti (fitness) antara GA dan Greedy baseline:
* **Metric Cards:** Menampilkan nilai penalti akhir masing-masing algoritma dan efisiensi peningkatan jadwal.
* **Charts:** Menampilkan diagram batang perbandingan total penalti dan rincian pelanggaran (Hard Constraint vs Soft Constraints).
* **Rincian JSON:** Menampilkan visualisasi data mentah pelanggaran untuk laporan analisis detail Anda.

### C. Evolusi Fitness
Halaman ini menampilkan grafik konvergensi perkembangan nilai fitness terbaik dari populasi di setiap generasi. Kurva meluruh ke bawah membuktikan keberhasilan eksplorasi operator mutasi/crossover hingga mencapai kestabilan (convergence).

---

## Tim Pengembang (Kelompok 17)

| Nama | NIM |
|------|-----|
| Husni Abdillah | G6401231097 |
| Daffa Aulia Musyaffa Subyantoro | G6401231028 |
| Qois Firosi | G6401231032 |
| Ghiffari Bravia Hisham | G6401231050 |
| Naufal Ghifari Afdhala | G6401231029 |