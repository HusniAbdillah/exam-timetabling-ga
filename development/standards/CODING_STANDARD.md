# Coding Standard

Dokumen ini mendefinisikan standar implementasi source code yang digunakan pada proyek **Optimasi Penjadwalan Ujian Universitas Menggunakan Genetic Algorithm**.

Seluruh anggota tim wajib mengikuti standar pada dokumen ini agar struktur kode tetap konsisten, mudah dipelihara, dan mudah diintegrasikan.

---

# 1. Tujuan

Standar ini disusun untuk:

* Menyamakan gaya penulisan kode.
* Mempermudah proses integrasi.
* Mengurangi merge conflict.
* Meningkatkan keterbacaan source code.
* Mempermudah proses pengujian.

---

# 2. Bahasa Pemrograman

Bahasa yang digunakan adalah Python.

Versi yang didukung:

```text
Python >= 3.11
Python < 3.14
```

Seluruh dependency dikelola menggunakan **uv**.

---

# 3. Struktur Source Code

Seluruh implementasi mengikuti struktur berikut.

```text
src/

config/
models/
preprocessing/
ga/
fitness/
evaluation/
visualization/
utils/
```

Tidak diperbolehkan membuat folder baru tanpa persetujuan seluruh anggota tim.

---

# 4. Penamaan

## File

Gunakan snake_case.

Contoh

```text
load_dataset.py
fitness_function.py
selection.py
```

---

## Class

Gunakan PascalCase.

Contoh

```text
Student
Course
Timeslot
GAResult
```

---

## Function

Gunakan snake_case.

Contoh

```text
calculate_fitness()

build_conflict_matrix()

load_students()
```

---

## Variable

Gunakan snake_case.

Contoh

```text
population

fitness_value

best_solution
```

---

## Constant

Gunakan huruf kapital.

Contoh

```text
POPULATION_SIZE

MAX_GENERATION

MUTATION_RATE
```

---

# 5. Type Hint

Seluruh function wajib menggunakan type hint.

Contoh

```python
def calculate_fitness(
    chromosome: Chromosome,
    conflict_matrix: ConflictMatrix,
) -> FitnessValue:
    ...
```

Function tanpa type hint tidak diperbolehkan.

---

# 6. Domain Model

Seluruh entitas utama menggunakan `@dataclass`.

Model yang digunakan:

* Student
* Course
* Enrollment
* Timeslot
* GAResult

Model tidak diperbolehkan menggunakan dictionary sebagai representasi utama.

---

# 7. Import

Urutan import mengikuti standar berikut.

1. Standard Library
2. Third Party Library
3. Local Module

Contoh

```python
from pathlib import Path

import pandas as pd

from src.models.student import Student
```

Wildcard import tidak diperbolehkan.

---

# 8. Path

Seluruh path menggunakan `pathlib.Path`.

Contoh

```python
from pathlib import Path

DATA_DIR = Path("data")
```

Penggunaan string untuk path dihindari.

---

# 9. Error Handling

Seluruh proses pembacaan dataset wajib menggunakan exception handling.

Contoh kasus:

* file tidak ditemukan
* format CSV tidak valid
* kolom tidak lengkap

Program tidak diperbolehkan berhenti tanpa memberikan pesan kesalahan yang jelas.

---

# 10. Logging

Gunakan modul `logging`.

Penggunaan `print()` hanya diperbolehkan pada proses demonstrasi menggunakan Streamlit.

---

# 11. Docstring

Seluruh class dan function publik wajib memiliki docstring.

Format yang digunakan mengikuti gaya Google Docstring.

Contoh

```python
def load_courses() -> list[Course]:
    """Memuat data mata kuliah dari dataset."""
```

---

# 12. Format Kode

Seluruh source code diformat menggunakan Ruff.

Perintah yang digunakan

```bash
uv run ruff format .
```

---

# 13. Linting

Seluruh source code harus lolos pemeriksaan Ruff.

Perintah

```bash
uv run ruff check .
```

Tidak diperbolehkan melakukan merge apabila masih terdapat error linting.

---

# 14. Testing

Seluruh modul utama wajib memiliki unit test.

Minimal modul yang diuji:

* preprocessing
* ga
* fitness

Framework yang digunakan adalah `pytest`.

Perintah

```bash
uv run pytest
```

---

# 15. Dependency

Dependency baru hanya boleh ditambahkan apabila benar-benar diperlukan.

Tidak diperbolehkan menambahkan library tanpa persetujuan Project Lead.

---

# 16. Aturan Modul

Setiap modul hanya memiliki satu tanggung jawab.

Sebagai contoh:

* `preprocessing` hanya membaca dan memvalidasi dataset.
* `ga` hanya menjalankan Genetic Algorithm.
* `fitness` hanya menghitung fitness.
* `evaluation` hanya mengevaluasi hasil.
* `visualization` hanya menampilkan hasil.

Tidak diperbolehkan memindahkan logika bisnis ke modul lain.

---

# 17. Aturan Integrasi

Seluruh komunikasi antar modul dilakukan melalui interface yang telah ditentukan pada `TYPE_GUIDELINES.md`.

Modul tidak diperbolehkan:

* membaca file milik modul lain secara langsung,
* mengubah struktur data modul lain,
* memodifikasi output modul lain.

---

# 18. Checklist Sebelum Commit

Sebelum melakukan commit, pastikan:

* Source code berhasil dijalankan.
* Ruff check berhasil.
* Ruff format telah dijalankan.
* Seluruh test berhasil.
* Tidak terdapat file sementara.
* Dokumentasi diperbarui apabila terdapat perubahan interface.

Dokumen ini menjadi acuan implementasi seluruh anggota tim selama proses pengembangan proyek.
