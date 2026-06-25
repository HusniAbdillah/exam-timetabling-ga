# Arsitektur Sistem

## Optimasi Penjadwalan Ujian Universitas Menggunakan Genetic Algorithm

---

# 1. Tujuan

Dokumen ini menjelaskan arsitektur perangkat lunak yang digunakan pada proyek Optimasi Penjadwalan Ujian Universitas Menggunakan Genetic Algorithm.

Arsitektur dirancang agar setiap modul memiliki tanggung jawab yang jelas, mudah diuji, serta memudahkan pengembangan secara paralel oleh seluruh anggota tim.

---

# 2. Prinsip Perancangan

Arsitektur proyek mengikuti beberapa prinsip berikut.

* Setiap modul hanya memiliki satu tanggung jawab (Single Responsibility Principle).
* Seluruh logika Genetic Algorithm dipisahkan dari antarmuka pengguna.
* Seluruh data dibaca dari dataset lokal.
* Tidak terdapat ketergantungan terhadap database maupun layanan eksternal.
* Seluruh modul dapat diuji secara independen.

---

# 3. Gambaran Arsitektur

```text
                 Dataset (CSV)
                        │
                        ▼
               Data Preprocessing
                        │
                        ▼
               Conflict Matrix Builder
                        │
                        ▼
             Genetic Algorithm Engine
                        │
                        ▼
               Fitness Evaluation
                        │
                        ▼
                  Best Schedule
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
    Evaluation                   Visualization
                        │
                        ▼
                  Streamlit App
```

---

# 4. Struktur Repository

```text
exam-timetabling-ga/

├── app/
├── data/
├── docs/
├── outputs/
├── src/
├── tests/

README.md
PRD.md
ARCHITECTURE.md
DATA_SPEC.md
TYPE_GUIDELINES.md
CODING_STANDARD.md
CONTRIBUTING.md
UV_SETUP.md
GIT_WORKFLOW.md
pyproject.toml
```

---

# 5. Struktur Source Code

```text
src/

├── preprocessing/
├── ga/
├── fitness/
├── evaluation/
├── visualization/
├── utils/
└── config/
```

---

# 6. Deskripsi Modul

## 6.1 preprocessing

Bertanggung jawab membaca dataset, melakukan validasi, serta membangun conflict matrix.

Tanggung jawab:

* membaca file CSV
* validasi data
* preprocessing
* membangun conflict matrix

Modul ini tidak mengetahui bagaimana Genetic Algorithm bekerja.

---

## 6.2 ga

Merupakan inti dari sistem.

Berisi implementasi Genetic Algorithm.

Komponen:

* chromosome
* population
* selection
* crossover
* mutation
* elitism
* engine

Modul ini tidak melakukan visualisasi maupun membaca file.

---

## 6.3 fitness

Menghitung kualitas suatu solusi.

Komponen:

* hard constraint
* soft constraint
* fitness evaluator

Modul ini hanya menerima chromosome dan conflict matrix.

---

## 6.4 evaluation

Melakukan evaluasi terhadap hasil optimasi.

Komponen:

* greedy baseline
* metrics
* benchmark

Output:

* nilai fitness
* runtime
* statistik konflik

---

## 6.5 visualization

Bertugas menampilkan hasil.

Komponen:

* grafik fitness
* tabel jadwal
* statistik

Modul ini tidak menghitung Genetic Algorithm.

---

## 6.6 utils

Berisi fungsi utilitas yang dapat digunakan bersama oleh seluruh modul.

Contoh:

* helper
* logger
* parser sederhana

---

## 6.7 config

Berisi konfigurasi proyek.

Contoh:

* ukuran populasi
* jumlah generasi
* mutation rate
* crossover rate

---

# 7. Alur Program

Urutan proses sistem adalah sebagai berikut.

1. Membaca dataset.
2. Melakukan validasi data.
3. Membangun conflict matrix.
4. Membentuk populasi awal.
5. Menjalankan Genetic Algorithm.
6. Menghitung fitness setiap individu.
7. Melakukan seleksi.
8. Melakukan crossover.
9. Melakukan mutation.
10. Membentuk populasi baru.
11. Mengulangi proses hingga generasi terakhir.
12. Menampilkan solusi terbaik.

---

# 8. Dependency Antar Modul

Hubungan antar modul dirancang satu arah.

```text
preprocessing
        │
        ▼
ga
        │
        ▼
fitness
        │
        ▼
evaluation
        │
        ▼
visualization
```

Modul pada level bawah tidak diperbolehkan mengakses modul pada level di atasnya.

Sebagai contoh:

* `ga` tidak boleh mengakses `visualization`.
* `fitness` tidak boleh membaca file CSV secara langsung.
* `visualization` tidak boleh menghitung fitness.

---

# 9. Antarmuka Pengguna

Aplikasi menggunakan Streamlit sebagai antarmuka sederhana.

Fitur yang disediakan:

* menampilkan ringkasan dataset
* konfigurasi parameter Genetic Algorithm
* menjalankan proses optimasi
* menampilkan grafik fitness
* menampilkan jadwal ujian
* menampilkan hasil evaluasi

---

# 10. Penyimpanan Data

Input berasal dari dataset lokal.

```text
data/

students.csv
courses.csv
enrollment.csv
timeslots.csv
```

Output disimpan pada direktori:

```text
outputs/

schedule.csv
fitness.csv
result.json
```

---

# 11. Arsitektur Pengembangan Tim

Setiap anggota bertanggung jawab terhadap satu modul utama.

| Anggota | Modul                     |
| ------- | ------------------------- |
| 1       | config, utils, integrasi  |
| 2       | preprocessing             |
| 3       | ga                        |
| 4       | fitness                   |
| 5       | evaluation, visualization |

Seluruh anggota tetap berkontribusi pada dokumentasi, pengujian, dan integrasi proyek.

---

# 12. Keputusan Arsitektur

Beberapa keputusan yang ditetapkan sejak awal proyek.

* Menggunakan Python.
* Menggunakan uv sebagai package manager.
* Menggunakan Streamlit sebagai antarmuka.
* Dataset dibaca dari file CSV lokal.
* Tidak menggunakan database.
* Tidak menggunakan Docker.
* Tidak menggunakan REST API.
* Tidak menggunakan room assignment.
* Fokus optimasi hanya pada penempatan ujian ke slot waktu.

Dokumen ini menjadi acuan utama selama proses pengembangan. Perubahan terhadap arsitektur hanya dapat dilakukan apabila disepakati oleh seluruh anggota tim.
