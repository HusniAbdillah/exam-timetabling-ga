# Git Workflow

Dokumen ini menjelaskan alur pengembangan menggunakan Git selama proyek berlangsung.

Seluruh anggota tim wajib mengikuti workflow ini agar proses pengembangan berjalan konsisten, mudah diintegrasikan, dan meminimalkan konflik.

---

# 1. Branch Strategy

Repository menggunakan dua branch utama.

```text
main
develop
```

Keterangan:

* **main** digunakan untuk versi stabil dan final.
* **develop** digunakan sebagai branch integrasi seluruh fitur.

Seluruh pengembangan dilakukan melalui branch `feature/*`.

---

# 2. Branch Pengembangan

Setiap anggota membuat branch berdasarkan modul yang dikerjakan.

Format penamaan:

```text
feature/<nama-modul>
```

Contoh:

```text
feature/preprocessing
feature/ga
feature/fitness
feature/evaluation
feature/visualization
feature/integration
```

Branch dibuat dari `develop`.

```bash
git checkout develop
git pull origin develop

git checkout -b feature/ga
```

---

# 3. Alur Pengembangan

Seluruh perubahan mengikuti alur berikut.

```text
                     main
                      ▲
                      │
                Merge Final
                      │
                   develop
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
 feature/preprocessing
 feature/ga
 feature/fitness
 feature/evaluation
 feature/visualization
 feature/integration
```

Urutan pengembangan:

1. Sinkronisasi branch `develop`.
2. Membuat branch `feature/*`.
3. Melakukan implementasi.
4. Menjalankan testing.
5. Commit perubahan.
6. Membuat Pull Request ke `develop`.
7. Code review.
8. Merge ke `develop`.
9. Setelah seluruh fitur selesai, merge `develop` ke `main`.

---

# 4. Workflow Harian

Sebelum mulai bekerja:

```bash
git checkout develop
git pull origin develop
```

Masuk ke branch masing-masing:

```bash
git checkout feature/ga
git merge develop
```

Apabila branch belum ada:

```bash
git checkout -b feature/ga
```

---

# 5. Aturan Commit

Lakukan commit dengan perubahan kecil dan spesifik.

Format commit:

```text
feat: menambahkan tournament selection
feat: menambahkan conflict matrix

fix: memperbaiki fitness evaluator
fix: memperbaiki parsing dataset

docs: memperbarui PRD
docs: memperbarui DATA_SPEC

refactor: merapikan preprocessing

test: menambahkan unit test fitness
```

Hindari commit seperti:

```text
update
fix
revisi
coba
123
final
```

---

# 6. Pull Request

Pull Request dibuat menuju branch `develop`.

Sebelum membuat Pull Request, pastikan:

* Source code berhasil dijalankan.
* Unit test berhasil.
* Ruff Check berhasil.
* Ruff Format telah dijalankan.
* Tidak terdapat konflik merge.
* Dokumentasi diperbarui apabila terdapat perubahan interface atau struktur data.

Template checklist:

```text
[ ] Program berhasil dijalankan
[ ] Unit test berhasil
[ ] Ruff check berhasil
[ ] Ruff format telah dijalankan
[ ] Dokumentasi diperbarui
```

---

# 7. Code Review

Minimal satu anggota tim melakukan review sebelum merge.

Review difokuskan pada:

* Kesesuaian dengan PRD.
* Kesesuaian dengan Architecture.
* Konsistensi interface.
* Kesesuaian dengan Data Specification.
* Kesesuaian dengan Type Guidelines.
* Kualitas implementasi.
* Keterbacaan kode.

Reviewer tidak diperbolehkan langsung melakukan perubahan pada branch milik anggota lain tanpa persetujuan.

---

# 8. Merge Policy

Merge dilakukan apabila:

* Pull Request telah direview.
* Tidak terdapat konflik merge.
* Seluruh checklist terpenuhi.
* Source code dapat dijalankan.

Merge langsung ke branch `main` tidak diperbolehkan.

---

# 9. Penyelesaian Konflik

Apabila terjadi konflik merge:

1. Sinkronkan branch dengan `develop`.
2. Selesaikan konflik secara lokal.
3. Jalankan kembali unit test.
4. Pastikan aplikasi tetap berjalan.
5. Commit hasil penyelesaian konflik.

Perubahan interface antar modul harus didiskusikan bersama sebelum dilakukan merge.

---

# 10. Definition of Done

Sebuah fitur dianggap selesai apabila:

* Seluruh implementasi telah selesai.
* Unit test tersedia dan berhasil dijalankan.
* Tidak terdapat error linting.
* Source code telah diformat.
* Dokumentasi telah diperbarui apabila diperlukan.
* Berhasil diintegrasikan dengan modul lain.
* Pull Request telah disetujui.

---

# 11. Branch Ownership

Setiap anggota memiliki branch utama sebagai berikut.

| Anggota  | Branch                |
| -------- | --------------------- |
| Person 1 | feature/integration   |
| Person 2 | feature/preprocessing |
| Person 3 | feature/ga            |
| Person 4 | feature/fitness       |
| Person 5 | feature/evaluation    |

Apabila diperlukan perubahan pada modul lain, koordinasikan terlebih dahulu dengan pemilik modul tersebut.

---

# 12. Praktik yang Disarankan

* Lakukan commit secara berkala dengan perubahan kecil.
* Hindari mengerjakan banyak fitur dalam satu commit.
* Selalu sinkronkan branch sebelum mulai bekerja.
* Jangan mengubah interface modul lain tanpa persetujuan.
* Pastikan seluruh perubahan dapat direproduksi oleh anggota tim lain menggunakan `uv sync`.

Dokumen ini menjadi acuan utama proses kolaborasi selama pengembangan proyek.
