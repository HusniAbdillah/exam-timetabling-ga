# Product Requirement Document (PRD)

## Optimasi Penjadwalan Ujian Universitas Menggunakan Genetic Algorithm

---

# 1. Pendahuluan

## 1.1 Latar Belakang

Penyusunan jadwal ujian merupakan salah satu permasalahan optimasi yang umum dijumpai pada lingkungan perguruan tinggi. Semakin banyak jumlah mahasiswa, program studi, serta mata kuliah yang diselenggarakan, semakin tinggi pula kemungkinan terjadinya konflik jadwal ujian.

Penyusunan jadwal secara manual membutuhkan waktu yang lama dan sulit menghasilkan jadwal yang optimal, terutama ketika terdapat banyak batasan (constraint) yang harus dipenuhi secara bersamaan.

Genetic Algorithm (GA) merupakan salah satu metode Evolutionary Computation yang banyak digunakan untuk menyelesaikan permasalahan optimasi kombinatorial seperti penjadwalan. Melalui mekanisme seleksi, crossover, dan mutation, Genetic Algorithm mampu mengeksplorasi ruang solusi untuk memperoleh jadwal dengan kualitas yang lebih baik.

Pada proyek ini, Genetic Algorithm diterapkan untuk mengoptimalkan penempatan setiap ujian ke dalam slot waktu berdasarkan konflik mahasiswa.

---

# 2. Tujuan

Proyek ini bertujuan untuk:

* Mengimplementasikan Genetic Algorithm pada permasalahan penjadwalan ujian.
* Menghasilkan jadwal ujian dengan konflik mahasiswa seminimal mungkin.
* Membandingkan hasil Genetic Algorithm dengan algoritma Greedy sebagai baseline.
* Menyediakan aplikasi demonstrasi yang mudah dipahami.

---

# 3. Ruang Lingkup

## In Scope

* Simulasi universitas multijurusan.
* Pembacaan dataset dari file CSV.
* Pembentukan conflict matrix.
* Implementasi Genetic Algorithm.
* Evaluasi fitness.
* Visualisasi hasil.
* Perbandingan dengan algoritma Greedy.

## Out of Scope

* Penjadwalan ruang ujian.
* Penjadwalan pengawas.
* Kapasitas ruang.
* Sistem informasi akademik.
* Basis data.
* REST API.
* Multi-objective optimization.

---

# 4. Studi Kasus

Universitas yang disimulasikan memiliki karakteristik sebagai berikut.

| Komponen                    |  Nilai |
| --------------------------- | -----: |
| Fakultas                    |     ±5 |
| Program Studi               |    ±10 |
| Mahasiswa per Program Studi |   ±130 |
| Mata Kuliah                 | ±40–60 |
| Slot Ujian                  |    ±15 |

Jenis mata kuliah terdiri atas:

* Mata kuliah umum universitas.
* Mata kuliah fakultas.
* Mata kuliah program studi.

Conflict antar ujian terbentuk berdasarkan mahasiswa yang mengambil lebih dari satu mata kuliah.

---

# 5. Permasalahan

Masalah utama yang diselesaikan adalah menentukan slot ujian untuk setiap mata kuliah sehingga konflik mahasiswa dapat diminimalkan.

Representasi solusi:

```text
Exam → Timeslot
```

Contoh:

| Mata Kuliah   | Slot |
| ------------- | ---- |
| Pancasila     | 1    |
| Struktur Data | 5    |
| Basis Data    | 8    |

---

# 6. Constraint

## Hard Constraint

Hard Constraint wajib dipenuhi.

* Mahasiswa tidak boleh memiliki dua ujian pada slot yang sama.

## Soft Constraint

Soft Constraint digunakan untuk meningkatkan kualitas jadwal.

* Mengurangi ujian berturut-turut.
* Mengurangi jumlah ujian dalam satu hari.
* Menyebarkan ujian secara lebih merata pada seluruh slot.

---

# 7. Dataset

Dataset disimpan dalam bentuk CSV.

| File           | Deskripsi                        |
| -------------- | -------------------------------- |
| students.csv   | Data mahasiswa                   |
| courses.csv    | Data mata kuliah                 |
| enrollment.csv | Relasi mahasiswa dan mata kuliah |
| timeslots.csv  | Slot ujian                       |

Seluruh dataset dibaca dari direktori `data/`.

---

# 8. Genetic Algorithm

Komponen yang diimplementasikan meliputi:

* Population Initialization
* Tournament Selection
* One Point Crossover
* Uniform Crossover
* Swap Mutation
* Move Mutation
* Elitism
* Fitness Evaluation

---

# 9. Baseline

Sebagai pembanding digunakan algoritma Greedy.

Tujuannya adalah memberikan gambaran peningkatan kualitas solusi yang dihasilkan Genetic Algorithm.

---

# 10. Output

Aplikasi menghasilkan:

* Jadwal ujian terbaik.
* Nilai fitness.
* Grafik perkembangan fitness.
* Statistik konflik.
* Perbandingan Genetic Algorithm dan Greedy.

---

# 11. Deliverables

Produk yang dihasilkan meliputi:

* Source Code
* Dataset
* Laporan
* Presentasi
* Video Demonstrasi

---

# 12. Kriteria Keberhasilan

Proyek dianggap berhasil apabila:

* Genetic Algorithm dapat dijalankan tanpa error.
* Jadwal ujian berhasil dihasilkan.
* Nilai fitness mengalami peningkatan selama proses evolusi.
* Hasil Genetic Algorithm lebih baik daripada algoritma Greedy.
* Seluruh deliverables proyek telah diselesaikan.
