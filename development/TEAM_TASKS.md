# Team Tasks

Dokumen ini menjelaskan pembagian tugas, kepemilikan modul, alur pengerjaan, serta target yang harus diselesaikan oleh setiap anggota tim selama pengembangan proyek **Optimasi Penjadwalan Ujian Universitas Menggunakan Genetic Algorithm**.

Seluruh anggota tim diharapkan mengikuti pembagian tugas ini agar proses pengembangan berjalan terstruktur dan setiap modul memiliki penanggung jawab yang jelas.

---

# 1. Tujuan

Dokumen ini bertujuan untuk:

* Menjelaskan pembagian tugas setiap anggota.
* Menentukan ownership setiap modul.
* Mengurangi overlap pekerjaan.
* Mempermudah proses integrasi.
* Menjadi acuan selama pengembangan proyek.

---

# 2. Timeline Proyek

| Minggu | Target                                           |
| ------ | ------------------------------------------------ |
| 1      | Setup repository, dokumentasi, generator dataset |
| 2      | Dataset, preprocessing, Genetic Algorithm        |
| 3      | Fitness, evaluasi, visualisasi                   |
| 4      | Integrasi, testing, laporan, presentasi          |

Timeline dapat disesuaikan berdasarkan perkembangan proyek.

---

# 3. Ownership Matrix

| Modul                 |  P1 |  P2 |  P3 |  P4 |  P5 |
| --------------------- | :-: | :-: | :-: | :-: | :-: |
| Repository            |  ✓  |     |     |     |     |
| Dokumentasi           |  ✓  |     |     |     |     |
| Config                |  ✓  |     |     |     |     |
| Utils                 |  ✓  |     |     |     |     |
| Streamlit Integration |  ✓  |     |     |     |     |
| Dataset Generator     |     |  ✓  |     |     |     |
| Dataset               |     |  ✓  |     |     |     |
| Preprocessing         |     |  ✓  |     |     |     |
| Conflict Matrix       |     |  ✓  |     |     |     |
| Models                |     |  ✓  |     |     |     |
| Genetic Algorithm     |     |     |  ✓  |     |     |
| Fitness               |     |     |     |  ✓  |     |
| Constraint            |     |     |     |  ✓  |     |
| Evaluation            |     |     |     |     |  ✓  |
| Visualization         |     |     |     |     |  ✓  |
| Baseline Greedy       |     |     |     |     |  ✓  |

---

# 4. Dependency Diagram

```text
Person 2
(Data Engineering)
        │
        ▼
Person 3
(Genetic Algorithm)
        │
        ▼
Person 4
(Fitness)
        │
        ▼
Person 5
(Evaluation & Visualization)

Person 1
(Project Lead)
mengintegrasikan seluruh modul
```

---

# 5. Person 1 — Project Lead & Integration

## Tanggung Jawab

* Menyiapkan struktur repository.
* Menjaga konsistensi arsitektur.
* Mengelola konfigurasi proyek.
* Mengintegrasikan seluruh modul.
* Menyusun dokumentasi utama.

### Ownership

```text
README.md
PRD.md
ARCHITECTURE.md

src/config/
src/utils/

app/
```

### Public Interface

* load_config()
* get_project_root()
* run_application()

### Deliverables

* Repository siap digunakan.
* Dokumentasi lengkap.
* Integrasi seluruh modul.

### Acceptance Criteria

* Seluruh modul berhasil dijalankan.
* Tidak terdapat konflik integrasi.
* Dokumentasi diperbarui.

---

# 6. Person 2 — Data Engineering

## Tanggung Jawab

* Membangun dataset simulasi universitas.
* Membuat generator dataset.
* Membuat preprocessing.
* Membangun conflict matrix.

### Ownership

```text
scripts/generate_dataset.py

src/models/

src/preprocessing/

data/
```

### Public Interface

* generate_dataset()
* load_dataset()
* validate_dataset()
* build_conflict_matrix()

### Deliverables

* students.csv
* courses.csv
* enrollment.csv
* timeslots.csv
* Conflict Matrix

### Acceptance Criteria

* Dataset valid.
* Generator berjalan.
* Conflict Matrix berhasil dibangun.

---

# 7. Person 3 — Genetic Algorithm

## Tanggung Jawab

* Mengembangkan Genetic Algorithm.
* Mengimplementasikan operator evolusi.

### Ownership

```text
src/ga/

chromosome.py
population.py
selection.py
crossover.py
mutation.py
elitism.py
engine.py
```

### Public Interface

* initialize_population()
* tournament_selection()
* one_point_crossover()
* uniform_crossover()
* swap_mutation()
* move_mutation()
* run_ga()

### Deliverables

* GA Engine
* Population
* Chromosome
* Operator Evolusi

### Acceptance Criteria

* GA dapat dijalankan.
* Fitness meningkat selama evolusi.
* Unit test berhasil.

---

# 8. Person 4 — Fitness & Constraint

## Tanggung Jawab

* Mengimplementasikan hard constraint.
* Mengimplementasikan soft constraint.
* Menghitung fitness.
* Menghasilkan statistik pelanggaran.

### Ownership

```text
src/fitness/
```

### Public Interface

* calculate_fitness()
* evaluate_constraints()
* calculate_penalty()

### Deliverables

* Fitness Evaluator
* Constraint Evaluator
* Statistik Pelanggaran

### Acceptance Criteria

* Hard constraint dihitung dengan benar.
* Soft constraint dihitung dengan benar.
* Fitness dapat digunakan oleh GA.

---

# 9. Person 5 — Evaluation & Visualization

## Tanggung Jawab

* Membuat baseline Greedy.
* Mengevaluasi hasil optimasi.
* Menampilkan visualisasi.
* Menyusun dashboard Streamlit.

### Ownership

```text
src/evaluation/

src/visualization/
```

### Public Interface

* run_greedy()
* evaluate_result()
* plot_fitness_history()
* build_schedule_table()

### Deliverables

* Baseline Greedy
* Grafik Fitness
* Tabel Jadwal
* Dashboard Streamlit

### Acceptance Criteria

* Greedy dapat dijalankan.
* Hasil GA dapat dibandingkan.
* Visualisasi berjalan dengan baik.

---

# 10. Definition of Done

Sebuah modul dianggap selesai apabila:

* Seluruh implementasi telah selesai.
* Unit test berhasil dijalankan.
* Ruff Check berhasil.
* Dokumentasi diperbarui apabila diperlukan.
* Berhasil diintegrasikan dengan modul lain.
* Pull Request telah disetujui.

---

# 11. Aturan Kolaborasi

Selama proses pengembangan:

* Setiap anggota hanya mengubah modul yang menjadi ownership-nya.
* Perubahan interface harus disepakati bersama.
* Integrasi dilakukan melalui branch `develop`.
* Seluruh perubahan mengikuti `CODING_STANDARD.md`.
* Seluruh dependency mengikuti `pyproject.toml`.

Dokumen ini menjadi acuan utama pembagian tugas selama proyek berlangsung.
