# Contributing Guide

Dokumen ini menjelaskan aturan kolaborasi selama proses pengembangan proyek **Optimasi Penjadwalan Ujian Universitas Menggunakan Genetic Algorithm**.

Seluruh anggota tim diharapkan mengikuti aturan pada dokumen ini agar proses pengembangan berjalan konsisten dan meminimalkan konflik integrasi.

---

# 1. Tujuan

Panduan ini bertujuan untuk:

* Menjaga konsistensi proses pengembangan.
* Mengurangi merge conflict.
* Mempermudah proses review.
* Memastikan setiap perubahan terdokumentasi dengan baik.

---

# 2. Branch Strategy

Branch utama yang digunakan:

```text
main
develop
```

Branch pengembangan menggunakan format berikut.

```text
feature/<nama-modul>
```

Contoh

```text
feature/preprocessing
feature/ga
feature/fitness
feature/evaluation
feature/visualization
feature/integration
```

Setiap anggota hanya bekerja pada branch miliknya.

---

# 3. Workflow

Urutan pengembangan proyek.

```text
develop
      │
      ▼
feature/*
      │
      ▼
Commit
      │
      ▼
Pull Request
      │
      ▼
Code Review
      │
      ▼
Merge ke develop
```

Branch `main` hanya diperbarui ketika proyek berada pada kondisi stabil.

---

# 4. Commit Message

Gunakan format commit berikut.

```text
feat: menambahkan tournament selection

fix: memperbaiki perhitungan fitness

docs: memperbarui DATA_SPEC

refactor: merapikan preprocessing

test: menambahkan unit test fitness
```

Hindari commit seperti:

```text
update

fix

coba

revisi

123
```

---

# 5. Pull Request

Sebelum membuat Pull Request, pastikan:

* Source code berhasil dijalankan.
* Seluruh test berhasil.
* Ruff check tidak menghasilkan error.
* Dokumentasi diperbarui apabila terdapat perubahan interface.

Pull Request harus memiliki deskripsi singkat mengenai perubahan yang dilakukan.

---

# 6. Code Review

Minimal satu anggota tim melakukan review sebelum proses merge.

Review difokuskan pada:

* Kesesuaian dengan PRD.
* Kesesuaian dengan Architecture.
* Konsistensi interface.
* Kualitas implementasi.
* Keterbacaan kode.

---

# 7. Merge Policy

Merge dilakukan apabila:

* Tidak terdapat konflik.
* Semua checklist Pull Request terpenuhi.
* Perubahan telah disetujui.

Merge langsung ke branch `main` tidak diperbolehkan.

---

# 8. Definition of Done

Sebuah fitur dianggap selesai apabila:

* Implementasi selesai.
* Unit test tersedia.
* Dokumentasi diperbarui apabila diperlukan.
* Tidak menghasilkan error linting.
* Berhasil diintegrasikan dengan modul lain.

---

# 9. Aturan Kolaborasi

Selama pengembangan proyek, seluruh anggota tim wajib:

* Mengikuti standar pada `CODING_STANDARD.md`.
* Mengikuti kontrak data pada `DATA_SPEC.md`.
* Mengikuti kontrak tipe data pada `TYPE_GUIDELINES.md`.
* Tidak mengubah interface modul lain tanpa persetujuan tim.
* Tidak melakukan merge tanpa proses review.

Dokumen ini menjadi pedoman kolaborasi selama pengembangan proyek.
