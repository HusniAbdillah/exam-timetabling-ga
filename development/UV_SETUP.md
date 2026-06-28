# UV Setup

Dokumen ini menjelaskan proses penyiapan environment pengembangan menggunakan **uv**.

Seluruh anggota tim wajib menggunakan environment yang sama untuk memastikan konsistensi dependency selama proses pengembangan.

---

# 1. Persyaratan

Sebelum memulai, pastikan telah tersedia:

* Git
* Python 3.11 atau lebih baru
* uv

---

# 2. Clone Repository

```bash
git clone https://github.com/HusniAbdillah/exam-timetabling-ga.git

cd exam-timetabling-ga
```

---

# 3. Sinkronisasi Dependency

Seluruh dependency dikelola melalui `pyproject.toml`.

Jalankan:

```bash
uv sync
```

Perintah tersebut akan:

* membuat virtual environment,
* memasang seluruh dependency,
* menghasilkan environment yang konsisten.

---

# 4. Menjalankan Aplikasi

```bash
uv run streamlit run app/app.py
```

---

# 5. Menjalankan Generator Dataset

Dataset dibuat satu kali menggunakan script berikut.

```bash
uv run python scripts/generate_dataset.py
```

Script tersebut akan menghasilkan dataset pada direktori:

```text
data/
```

Dataset yang telah dihasilkan disimpan ke dalam repository dan digunakan oleh seluruh anggota tim.

Script ini **tidak dijalankan sebagai bagian dari aplikasi**.

---

# 6. Menjalankan Unit Test

```bash
uv run pytest
```

---

# 7. Menjalankan Ruff

Format source code

```bash
uv run ruff format .
```

Linting

```bash
uv run ruff check .
```

---

# 8. Update Dependency

Apabila diperlukan dependency baru

```bash
uv add <package>
```

Setelah dependency berubah

```bash
uv lock
```

Commit perubahan berikut.

* pyproject.toml
* uv.lock

---

# 9. Catatan

Seluruh anggota tim wajib menggunakan dependency yang berasal dari repository.

Tidak diperbolehkan memasang dependency secara manual tanpa memperbarui `pyproject.toml`.

Dokumen ini menjadi acuan penyiapan environment selama proses pengembangan.
