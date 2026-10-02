# The Inkwell Development Roadmap

**Version:** 1.0.0

> Dokumen ini menjadi patokan utama development Inkwell.
> Codex/development agent harus mengikuti urutan phase dan checkpoint di dokumen ini.

---

## Phase 0 — Project Foundation

### Tujuan
Menyiapkan fondasi proyek.

### Deliverables
- Project bisa dijalankan.
- Struktur folder selesai.
- Git repository siap.
- Virtual environment siap.
- Requirements siap.

### Definition of Done
`python main.py` membuka window kosong.

---

## Phase 1 — Database Foundation

### Tujuan
Membangun sistem penyimpanan data.

### Deliverables
- SQLite berjalan.
- SQLAlchemy berjalan.
- Model:
  - Book
  - Note
  - Quote
  - ReadingSession
  - Scratchpad
  - Audio
  - Settings
- Database otomatis dibuat.

### Definition of Done
Bisa Create, Read, Update, Delete Book melalui script test.

---

## Phase 2 — Application Shell

### Tujuan
Membangun kerangka aplikasi.

### Deliverables
- Main Window.
- Sidebar.
- Navigation.
- Page Switching.
- Theme System.

### Definition of Done
User dapat berpindah Library, Journal, Statistics, Focus Mode, dan Settings tanpa error.

---

## Phase 3 — Library Module

### Tujuan
Membangun perpustakaan pribadi.

### Deliverables
- Add Book.
- Edit Book.
- Delete Book.
- Book Grid.
- Book Detail.
- Status Book.

### Definition of Done
User dapat mengelola buku sepenuhnya secara manual.

---

## Phase 4 — Online Book Search

### Tujuan
Mengurangi input manual.

### Deliverables
- Google Books API.
- Open Library API.
- Search Dialog.
- Import Book.
- Cover Download.
- Cover Cache.

### Definition of Done
User mengetik `Atomic Habits`, lalu buku masuk ke Library hanya dengan satu klik.

---

## Phase 5 — Journal Module

### Tujuan
Menyimpan hasil pemikiran.

### Deliverables
- Create Note.
- Edit Note.
- Delete Note.
- Create Quote.
- Search Notes.
- Book Relation.

### Definition of Done
Semua catatan dapat dihubungkan ke buku.

---

## Phase 6 — Reading Session Engine

### Tujuan
Melacak aktivitas membaca.

### Deliverables
- Start Session.
- End Session.
- Page Tracking.
- Duration Tracking.
- Session History.

### Definition of Done
User dapat melihat seluruh riwayat membaca.

---

## Phase 7 — Statistics Engine

### Tujuan
Mengubah data menjadi insight.

### Deliverables
- Total Books.
- Books Finished.
- Reading Time.
- Pages Read.
- Reading Streak.
- Genre Chart.
- Heatmap.
- Monthly Activity.

### Definition of Done
Dashboard statistik berfungsi penuh.

---

## Phase 8 — Focus Mode Core

### Tujuan
Membangun fitur utama The Inkwell.

### Deliverables
- Fullscreen Mode.
- Focus Layout.
- Theme Switching.
- Focus Notes.
- Autosave.

### Definition of Done
User dapat membaca dan mencatat dalam Focus Mode.

---

## Phase 9 — Focus Timer

### Tujuan
Mendukung sesi membaca fokus.

### Deliverables
- Pomodoro.
- Custom Timer.
- Session Tracking.
- Timer Statistics.

### Definition of Done
Timer terintegrasi dengan Reading Session.

---

## Phase 10 — Audio System

### Tujuan
Menambahkan suasana membaca.

### Deliverables
- Import MP3.
- Playlist.
- Play.
- Pause.
- Volume.

### Definition of Done
Audio lokal berjalan stabil.

### Current Status
**COMPLETED**

Implementasi checkpoint saat ini:
- `app/services/audio_service.py`
- `app/ui/components/audio_player_widget.py`
- Integrasi Audio Player ke Focus Mode.

Commit:
`cb35e05 feat: add audio player to focus mode`

Catatan:
- Audio lokal sudah terintegrasi dengan Focus Mode.
- Playback perangkat audio nyata belum diverifikasi di environment development.
- Database/Alembic tidak berubah pada checkpoint ini.

---

## Phase 11 — Settings & Backup

### Tujuan
Menyelesaikan kebutuhan sistem.

### Deliverables
- Theme Settings.
- Storage Settings.
- Backup Database.
- Restore Database.

### Definition of Done
User dapat mem-backup seluruh data.

### Current Status
**COMPLETED**

---

## Phase 12 — Visual Polish

### Tujuan
Membuat aplikasi terasa selesai.

### Deliverables
- Visual Identity diterapkan penuh.
- Ink & Paper Aesthetic.
- Sketchbook Focus Themes.
- Icon System.
- Spacing Cleanup.
- Typography Cleanup.

### Definition of Done
Aplikasi terlihat seperti The Inkwell.

### Current Status
**COMPLETED**

---

## Phase 13 — Release Preparation

### Tujuan
Menyiapkan distribusi.

### Deliverables
- Testing.
- Bug Fixing.
- Log System.
- Windows Build.
- Linux Build.
- Installer.

### Build Commands
- Windows bundle: install `requirements-build-windows.txt` and run `build_windows.ps1`.
- Windows installer: set the canonical MAJOR.MINOR.PATCH version in `VERSION`, install Inno Setup 6, then run `build_windows.ps1 -CreateInstaller` (or pass a custom `ISCC.exe` path with `-InnoSetupCompiler`).
- Linux: install `requirements-build-linux.txt`, make `appimagetool` available on `PATH` (or set `APPIMAGETOOL`), then run `./build_linux.sh`.

### Definition of Done
Menghasilkan:
- `TheInkwell.AppImage`
- `TheInkwellSetup.exe`

### Current Status
**NEXT**

---

# MVP Completion Checklist

Versi 1.0.0 dianggap selesai ketika pengguna dapat:

1. Add Book
2. Search Book Online
3. Store Book
4. Write Notes
5. Save Quotes
6. Track Reading Sessions
7. View Statistics
8. Enter Focus Mode
9. Use Timer
10. Play Local Music
11. Backup Data

---

# Development Rules

## 1. Ikuti Urutan Phase
Development mengikuti Phase 0 → Phase 13. Jangan melompati phase tanpa instruksi eksplisit.

## 2. Satu Checkpoint Sekaligus
Selesaikan satu checkpoint/fitur sebelum berpindah ke checkpoint berikutnya.

## 3. Audit Secukupnya
Audit dilakukan ketika:
- mulai mengerjakan satu fitur baru; atau
- ditemukan error saat menjalankan aplikasi/test.

Tidak perlu audit besar setelah setiap perubahan kecil jika fitur berjalan sesuai contract.

## 4. Pertahankan Fitur Lama
Jangan mengubah perilaku fitur lama tanpa alasan yang jelas. Jika perubahan behavior diperlukan, laporkan sebelum perubahan signifikan.

## 5. Database dan Alembic
Jangan mengubah model, migration, schema, atau database existing kecuali fitur memang membutuhkan perubahan tersebut. Jangan reset database.

## 6. Verification
Setiap checkpoint lakukan verification yang relevan, minimal bila sesuai:
- `py_compile`
- `git diff --check`
- smoke test

## 7. Commit
Agent tidak membuat commit kecuali diminta secara eksplisit.

Setelah checkpoint selesai, laporkan:
- file yang dibuat/diubah,
- fungsi yang diubah,
- verification,
- risiko/keputusan yang masih terbuka,
- status Git.

## 8. Jangan Mengarang Roadmap
Jika checkpoint berikutnya tidak tersedia di dokumen ini, STOP dan laporkan. Jangan memilih fitur sendiri berdasarkan tebakan repository.

---

# Current Development Position

- Phase 0 — COMPLETED
- Phase 1 — COMPLETED
- Phase 2 — COMPLETED
- Phase 3 — COMPLETED
- Phase 4 — COMPLETED
- Phase 5 — COMPLETED
- Phase 6 — COMPLETED
- Phase 7 — COMPLETED
- Phase 8 — COMPLETED
- Phase 9 — COMPLETED
- Phase 10 — COMPLETED
- Phase 11 — COMPLETED
- Phase 12 — COMPLETED
- Phase 13 — NEXT

**Next Phase: Phase 13 — Release Preparation**
