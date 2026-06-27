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
```

---

# 3. students.csv

Menyimpan informasi mahasiswa.

| Field         | Tipe    | Keterangan        |
| ------------- | ------- | ----------------- |
| student_id    | string  | ID unik mahasiswa |
| department_id | string  | Program studi     |
| semester      | integer | Semester aktif    |

Contoh

| student_id | department_id | semester |
| ---------- | ------------- | -------- |
| S0001      | IF            | 4        |
| S0002      | IF            | 4        |
| S0101      | ST            | 2        |

---

# 4. courses.csv

Menyimpan informasi mata kuliah.

| Field         | Tipe    | Keterangan                        |
| ------------- | ------- | --------------------------------- |
| course_id     | string  | ID mata kuliah                    |
| course_name   | string  | Nama mata kuliah                  |
| department_id | string  | Program studi pemilik             |
| semester      | integer | Semester penyelenggaraan          |
| course_type   | string  | GENERAL, FACULTY, atau DEPARTMENT |

Contoh

| course_id | course_name   | department_id | semester | course_type |
| --------- | ------------- | ------------- | -------- | ----------- |
| IF301     | Struktur Data | IF            | 3        | DEPARTMENT  |
| MKU101    | Pancasila     | GENERAL       | 1        | GENERAL     |

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

# 7. Model Data

Seluruh modul menggunakan model berikut.

## Student

| Field         | Tipe   |
| ------------- | ------ |
| student_id    | string |
| department_id | string |
| semester      | int    |

---

## Course

| Field         | Tipe   |
| ------------- | ------ |
| course_id     | string |
| course_name   | string |
| department_id | string |
| semester      | int    |
| course_type   | string |

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

Output

* Student
* Course
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

Output

* Fitness Value (Evaluasi Pinalti)

### Rumus Evaluasi Penalti
Optimasi dilakukan dengan meminimalkan total penalti (*lower penalty is better*). Rumus perhitungan penalti didefinisikan sebagai:

$$\text{penalty} = 1000 \times \text{Hard Constraint} + 10 \times \text{Consecutive Exams} + 5 \times \text{Too Many Exams Per Day} + 2 \times \text{Spread Penalty}$$

Di mana:
* **Hard Constraint**: Jumlah mahasiswa yang memiliki jadwal ujian bentrok (pada slot yang sama).
* **Consecutive Exams**: Jumlah kejadian mahasiswa memiliki ujian berurutan/berturut-turut pada hari yang sama.
* **Too Many Exams Per Day**: Jumlah kejadian mahasiswa memiliki lebih dari dua ujian dalam satu hari.
* **Spread Penalty**: Penalti penyebaran ujian untuk mengukur ketidakmerataan distribusi ujian pada slot waktu yang tersedia.

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
| best_fitness | float | Nilai fitness (penalti) terbaik pada generasi tersebut |

Contoh isi:
```csv
generation,best_fitness
0,1520.0
1,1210.0
2,850.0
```

### 13.3 statistics.json
Menyimpan perbandingan performa antara algoritma Genetic Algorithm (GA) dan Greedy baseline, beserta rincian pelanggaran batasannya (constraint).

Format berkas JSON:
```json
{
  "ga": {
    "execution_time_seconds": float,
    "best_fitness": float,
    "hard_constraint_violations": integer,
    "consecutive_exams_violations": integer,
    "too_many_exams_violations": integer,
    "spread_penalty": float
  },
  "greedy": {
    "execution_time_seconds": float,
    "best_fitness": float,
    "hard_constraint_violations": integer,
    "consecutive_exams_violations": integer,
    "too_many_exams_violations": integer,
    "spread_penalty": float
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
