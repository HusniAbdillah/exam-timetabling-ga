# Data Specification

Dokumen ini mendefinisikan struktur dataset, model data, serta kontrak pertukaran data antar modul pada proyek **Optimasi Penjadwalan Ujian Universitas Menggunakan Genetic Algorithm**.

Seluruh anggota tim wajib mengikuti spesifikasi pada dokumen ini. Perubahan terhadap struktur data hanya dapat dilakukan melalui kesepakatan seluruh anggota tim.

---

# 1. Gambaran Umum

Sistem menggunakan dataset lokal dalam format CSV.

Dataset merepresentasikan sebuah universitas yang terdiri atas beberapa fakultas, program studi, mahasiswa, mata kuliah, serta slot ujian.

Seluruh modul menggunakan dataset yang sama sebagai sumber data utama.

---

# 2. Struktur Dataset

```text
data/

students.csv
courses.csv
enrollment.csv
timeslots.csv
rooms.csv
slot_blocks.csv
```

---

# 3. students.csv

Menyimpan informasi mahasiswa.

| Field            | Tipe    | Keterangan        |
| ---------------- | ------- | ----------------- |
| student_id       | string  | ID unik mahasiswa |
| faculty_id       | string  | Fakultas          |
| department_id    | string  | Program studi     |
| current_semester | integer | Semester aktif    |

Contoh

| student_id | faculty_id | department_id | current_semester |
| ---------- | ---------- | ------------- | ---------------- |
| S0001      | FMIPA      | IF            | 4                |
| S0002      | FMIPA      | IF            | 4                |
| S0101      | FMIPA      | ST            | 2                |

---

# 4. courses.csv

Menyimpan informasi mata kuliah.

| Field            | Tipe    | Keterangan                                  |
| ---------------- | ------- | ------------------------------------------- |
| course_id        | string  | ID mata kuliah                              |
| course_name      | string  | Nama mata kuliah                            |
| faculty_id       | string  | Fakultas yang menawarkan                    |
| department_id    | string  | Program studi pemilik                       |
| offered_semester | integer | Semester penyelenggaraan                    |
| course_type      | string  | GENERAL, FACULTY, DEPARTMENT, atau ELECTIVE |
| room_id          | string  | ID ruangan yang dialokasikan                |

Contoh

| course_id | course_name   | faculty_id | department_id | offered_semester | course_type | room_id |
| --------- | ------------- | ---------- | ------------- | ---------------- | ----------- | ------- |
| IF301     | Struktur Data | FMIPA      | IF            | 3                | DEPARTMENT  | R001    |
| MKU101    | Pancasila     | GENERAL    | GENERAL       | 1                | GENERAL     | R002    |

---

# 5. enrollment.csv

Relasi mahasiswa dan mata kuliah.

Satu baris menunjukkan bahwa seorang mahasiswa mengambil satu mata kuliah.

| Field      | Tipe   | Keterangan   |
| ---------- | ------ | ------------ |
| student_id | string | ID mahasiswa |
| course_id  | string | Mata kuliah  |

Contoh

| student_id | course_id |
| ---------- | --------- |
| S0001      | IF301     |
| S0001      | MKU101    |
| S0001      | IF302     |

---

# 6. timeslots.csv

Daftar slot ujian yang tersedia.

| Field   | Tipe    | Keterangan              |
| ------- | ------- | ----------------------- |
| slot_id | integer | Nomor slot              |
| day     | integer | Hari ujian              |
| session | integer | Sesi pada hari tersebut |

Contoh

| slot_id | day | session |
| ------- | --- | ------- |
| 1       | 1   | 1       |
| 2       | 1   | 2       |
| 3       | 2   | 1       |

---

# 6a. rooms.csv

Menyimpan informasi kapasitas ruangan.

| Field   | Tipe    | Keterangan        |
| ------- | ------- | ----------------- |
| room_id | string  | ID unik ruangan   |
| capacity| integer | Kapasitas ruangan |

Contoh

| room_id | capacity |
| ------- | -------- |
| R001    | 300      |
| R002    | 150      |

---

# 6b. slot_blocks.csv

Menyimpan informasi pemblokiran slot ujian untuk fakultas tertentu.

| Field      | Tipe    | Keterangan              |
| ---------- | ------- | ----------------------- |
| faculty_id | string  | ID fakultas             |
| day        | integer | Hari ujian yang diblok  |
| session    | integer | Sesi ujian yang diblok  |

Contoh

| faculty_id | day | session |
| ---------- | --- | ------- |
| FMIPA      | 1   | 1       |
| FATETA     | 2   | 2       |

---

# 7. Model Data

Seluruh modul menggunakan model berikut.

## Student

| Field            | Tipe   |
| ---------------- | ------ |
| student_id       | string |
| faculty_id       | string |
| department_id    | string |
| current_semester | int    |

---

## Course

| Field            | Tipe   |
| ---------------- | ------ |
| course_id        | string |
| course_name      | string |
| faculty_id       | string |
| department_id    | string |
| offered_semester | int    |
| course_type      | string |
| room_id          | string |

---

## Room

| Field    | Tipe   |
| -------- | ------ |
| room_id  | string |
| capacity | int    |

---

## Enrollment

| Field      | Tipe   |
| ---------- | ------ |
| student_id | string |
| course_id  | string |

---

## Timeslot

| Field   | Tipe |
| ------- | ---- |
| slot_id | int  |
| day     | int  |
| session | int  |

---

# 8. Conflict Matrix

Conflict Matrix merupakan representasi hubungan konflik antar mata kuliah.

Dua mata kuliah dikatakan memiliki konflik apabila terdapat minimal satu mahasiswa yang mengambil keduanya.

Representasi logis:

```text
Course A
↓

Student

↓

Course B
```

Contoh

```text
IF301

↓

S0001

↓

IF302
```

Maka

```text
IF301 ↔ IF302
```

---

# 9. Representasi Internal

Conflict Matrix direpresentasikan sebagai adjacency list.

Contoh

```python
{
    "IF301": {"IF302", "MKU101"},
    "IF302": {"IF301"},
    "MKU101": {"IF301"}
}
```

Representasi ini dipilih karena lebih efisien dibanding adjacency matrix untuk jumlah mata kuliah yang relatif sedikit.

---

# 10. Representasi Chromosome

Satu chromosome merepresentasikan satu solusi penjadwalan.

Struktur

```text
Index
↓

Course

Value
↓

Timeslot
```

Contoh

```text
[3, 1, 5, 2]
```

Artinya

| Course   | Slot |
| -------- | ---- |
| Course 1 | 3    |
| Course 2 | 1    |
| Course 3 | 5    |
| Course 4 | 2    |

Urutan course ditentukan berdasarkan urutan pada `courses.csv`.

---

# 11. Population

Population merupakan kumpulan chromosome.

Representasi

```text
Population

├── Chromosome 1
├── Chromosome 2
├── Chromosome 3
└── ...
```

---

# 12. Input Modul

## preprocessing

Input

* students.csv
* courses.csv
* enrollment.csv
* timeslots.csv
* rooms.csv
* slot_blocks.csv

Output

* Student
* Course
* Room
* Enrollment
* Timeslot
* Conflict Matrix

---

## ga

Input

* Conflict Matrix
* Timeslot
* Parameter GA

Output

* GAResult

---

## fitness

Input

* Chromosome
* Conflict Matrix
* Rooms data
* Slot Blocks data

Output

* Fitness Value (Evaluasi Penalti)

### Rumus Evaluasi Penalti
Optimasi dilakukan dengan meminimalkan total penalti (*lower penalty is better*). Rumus perhitungan penalti didefinisikan sebagai:

$$\text{penalty} = 1000 \times \text{Hard Constraint} + 10 \times \text{Consecutive Exams} + 5 \times \text{Too Many Exams Per Day} + 30 \times \text{Spread Penalty} + 3 \times \text{Same Semester Core Separation} + 2 \times \text{High Enrollment Exam Separation} + 1 \times \text{Preferred Gap} + 200 \times \text{Max Exams Per Day Violations} + 300 \times \text{Room Capacity Violations} + 250 \times \text{Slot Block Violations}$$

Di mana:
* **Hard Constraint**: Jumlah mahasiswa yang memiliki jadwal ujian bentrok (pada slot yang sama).
* **Consecutive Exams**: Jumlah kejadian mahasiswa memiliki ujian berurutan/berturut-turut pada hari yang sama.
* **Too Many Exams Per Day**: Jumlah kejadian mahasiswa memiliki lebih dari dua ujian dalam satu hari.
* **Spread Penalty**: Penalti penyebaran ujian untuk mengukur ketidakmerataan distribusi ujian pada slot waktu yang tersedia.
* **Same Semester Core Separation**: Penalti ketika mata kuliah wajib pada semester dan jurusan yang sama dijadwalkan pada hari yang sama atau berurutan.
* **High Enrollment Exam Separation**: Penalti ketika beberapa mata kuliah umum/besar dijadwalkan pada hari yang sama.
* **Preferred Gap**: Penalti ketika mahasiswa memiliki ujian di sesi yang berurutan tanpa jeda minimal satu slot kosong.
* **Max Exams Per Day Violations**: Penalti ketika mahasiswa melebihi batas maksimal ujian per hari (default: 2 ujian per hari).
* **Room Capacity Violations**: Penalti ketika kapasitas ruang ujian terlampaui oleh jumlah mahasiswa terdaftar dalam slot/ruangan tersebut.
* **Slot Block Violations**: Penalti ketika ujian dijadwalkan pada slot yang diblokir oleh fakultas (dosen tidak bersedia/bentrok).

---

## evaluation

Input

* GAResult

Output

* EvaluationResult

---

## visualization

Input

* GAResult
* EvaluationResult

Output

* Tabel Jadwal
* Grafik Fitness
* Ringkasan Hasil

---

# 13. Output Program

Program menghasilkan beberapa berkas pada direktori `outputs/`.

```text
outputs/

schedule.csv
fitness_history.csv
statistics.json
```

### 13.1 schedule.csv
Menyimpan hasil pemetaan mata kuliah ke slot waktu ujian yang terpilih.

| Field | Tipe | Keterangan |
| --- | --- | --- |
| course_id | string | ID mata kuliah |
| course_name | string | Nama mata kuliah |
| slot_id | integer | ID slot waktu ujian |
| day | integer | Hari ujian |
| session | integer | Sesi ujian |

Contoh isi:
```csv
course_id,course_name,slot_id,day,session
IF301,Struktur Data,5,2,1
MKU101,Pancasila,1,1,1
```

### 13.2 fitness_history.csv
Menyimpan perkembangan nilai fitness (penalti terbaik) dari setiap generasi selama GA berjalan.

| Field | Tipe | Keterangan |
| --- | --- | --- |
| generation | integer | Generasi ke-n (0-indexed) |
| pure_ga_fitness | float | Nilai fitness (penalti) terbaik Pure GA pada generasi tersebut |
| hybrid_ga_fitness | float | Nilai fitness (penalti) terbaik Hybrid GA pada generasi tersebut |

Contoh isi:
```csv
generation,pure_ga_fitness,hybrid_ga_fitness
0,1520.0,1200.0
1,1210.0,900.0
2,850.0,600.0
```

### 13.3 statistics.json
Menyimpan perbandingan performa antara algoritma Pure Genetic Algorithm (Pure GA), Hybrid Genetic Algorithm (Hybrid GA), dan Greedy baseline, beserta rincian pelanggaran batasannya (constraint).

Format berkas JSON:
```json
{
  "pure_ga": {
    "execution_time_seconds": float,
    "best_fitness": float,
    "hard_constraint_violations": integer,
    "consecutive_exams_violations": integer,
    "too_many_exams_violations": integer,
    "spread_penalty": float,
    "max_exams_per_day_violations": integer,
    "room_capacity_violations": integer,
    "slot_block_violations": integer
  },
  "hybrid_ga": {
    "execution_time_seconds": float,
    "best_fitness": float,
    "hard_constraint_violations": integer,
    "consecutive_exams_violations": integer,
    "too_many_exams_violations": integer,
    "spread_penalty": float,
    "max_exams_per_day_violations": integer,
    "room_capacity_violations": integer,
    "slot_block_violations": integer
  },
  "greedy": {
    "execution_time_seconds": float,
    "best_fitness": float,
    "hard_constraint_violations": integer,
    "consecutive_exams_violations": integer,
    "too_many_exams_violations": integer,
    "spread_penalty": float,
    "max_exams_per_day_violations": integer,
    "room_capacity_violations": integer,
    "slot_block_violations": integer
  }
}
```

---

# 14. Validasi Dataset

Dataset dianggap valid apabila memenuhi kondisi berikut.

* Seluruh `student_id` unik.
* Seluruh `course_id` unik.
* Seluruh relasi enrollment mengacu pada mahasiswa dan mata kuliah yang valid.
* Minimal terdapat satu slot ujian.
* Tidak terdapat nilai kosong pada field wajib.

---

# 15. Kontrak Data

Seluruh modul wajib mengikuti kontrak berikut.

* Dataset hanya dibaca oleh modul `preprocessing`.
* Modul lain tidak diperbolehkan membaca file CSV secara langsung.
* Conflict Matrix hanya dibuat oleh `preprocessing`.
* Chromosome hanya dibuat dan dimodifikasi oleh modul `ga`.
* Fitness hanya dihitung oleh modul `fitness`.
* Visualisasi tidak boleh menghitung ulang fitness.
* Evaluasi tidak boleh memodifikasi chromosome.

Dokumen ini menjadi acuan utama seluruh implementasi proyek.
