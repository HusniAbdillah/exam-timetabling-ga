# Type Guidelines

Dokumen ini mendefinisikan tipe data, alias tipe, serta aturan representasi data yang digunakan pada seluruh proyek.

Seluruh implementasi wajib mengikuti spesifikasi pada dokumen ini agar setiap modul memiliki antarmuka yang konsisten.

---

# 1. Tujuan

Dokumen ini bertujuan untuk:

* Menyamakan representasi data pada seluruh modul.
* Mengurangi konflik integrasi antar anggota tim.
* Menjadi acuan implementasi type hint pada Python.
* Memastikan seluruh modul memiliki interface yang konsisten.

---

# 2. Aturan Umum

Seluruh source code wajib menggunakan:

* Python Type Hint
* `typing.TypeAlias`
* `dataclass` untuk domain model
* `pathlib.Path` untuk pengelolaan path

Tipe data bawaan Python tetap digunakan apabila sudah memadai.

---

# 3. Primitive Alias

Seluruh identifier direpresentasikan sebagai `str`.

| Alias        | Tipe |
| ------------ | ---- |
| StudentId    | str  |
| CourseId     | str  |
| DepartmentId | str  |
| FacultyId    | str  |

Identifier slot direpresentasikan sebagai integer.

| Alias      | Tipe |
| ---------- | ---- |
| TimeslotId | int  |
| Day        | int  |
| Session    | int  |

Nilai fitness direpresentasikan sebagai floating point.

| Alias        | Tipe  |
| ------------ | ----- |
| FitnessValue | float |

---

# 4. Collection Alias

Representasi collection yang digunakan pada proyek.

| Alias          | Tipe               |
| -------------- | ------------------ |
| Chromosome     | list[int]          |
| Population     | list[Chromosome]   |
| FitnessHistory | list[FitnessValue] |

---

# 5. Conflict Matrix

Conflict Matrix direpresentasikan sebagai adjacency list.

Representasi logis

```python
dict[CourseId, set[CourseId]]
```

Contoh

```python
{
    "IF301": {"IF302", "MKU101"},
    "IF302": {"IF301"},
    "MKU101": {"IF301"}
}
```

Representasi ini digunakan pada seluruh modul.

---

# 6. Domain Model

Seluruh entitas utama direpresentasikan menggunakan `@dataclass`.

Model yang digunakan:

* Student
* Course
* Enrollment
* Timeslot
* GAResult

Selain model di atas, implementasi tidak diperbolehkan membuat representasi data baru tanpa persetujuan tim.

---

# 7. Chromosome

Chromosome merupakan representasi solusi.

Representasi

```python
list[int]
```

Posisi indeks menunjukkan urutan mata kuliah.

Nilai pada indeks menunjukkan slot ujian.

Contoh

```python
[3, 1, 5, 2]
```

Artinya

| Course Index | Slot |
| ------------ | ---- |
| 0            | 3    |
| 1            | 1    |
| 2            | 5    |
| 3            | 2    |

---

# 8. Population

Population merupakan kumpulan chromosome.

Representasi

```python
list[Chromosome]
```

Seluruh operator Genetic Algorithm bekerja pada struktur data ini.

---

# 9. GAResult

Seluruh proses optimasi menghasilkan satu objek `GAResult`.

Objek tersebut minimal memiliki informasi berikut.

| Field           | Tipe           |
| --------------- | -------------- |
| best_solution   | Chromosome     |
| best_fitness    | FitnessValue   |
| fitness_history | FitnessHistory |
| generation      | int            |
| execution_time  | float          |

Dengan menggunakan model ini, fungsi Genetic Algorithm cukup mengembalikan satu objek tanpa perlu mengembalikan banyak nilai secara terpisah.

---

# 10. Interface Antar Modul

## preprocessing

Output

* Student
* Course
* Enrollment
* Timeslot
* ConflictMatrix

---

## ga

Input

* ConflictMatrix
* Timeslot
* Parameter GA

Output

* GAResult

---

## fitness

Input

* Chromosome
* ConflictMatrix

Output

* FitnessValue

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

* Grafik
* Tabel
* Statistik

---

# 11. Aturan Integrasi

Untuk menjaga konsistensi implementasi, seluruh anggota tim wajib mengikuti aturan berikut.

* Tidak mengubah tipe data yang telah ditetapkan.
* Tidak membuat representasi data baru tanpa diskusi tim.
* Tidak mengubah struktur `GAResult`.
* Tidak mengubah representasi `Chromosome`.
* Tidak mengubah representasi `ConflictMatrix`.

Seluruh perubahan terhadap kontrak data harus disepakati oleh seluruh anggota tim sebelum diimplementasikan.
