"""
File:
    book_status.py

Purpose:
    Menyimpan seluruh status buku yang digunakan di aplikasi.

Responsibilities:
    - Menyediakan konstanta status buku
    - Menyediakan daftar seluruh status

Does NOT:
    - Menyimpan logika aplikasi
"""


class BookStatus:

    READING = "Reading"

    WANT_TO_READ = "Want To Read"

    COMPLETED = "Completed"

    PAUSED = "Paused"

    DROPPED = "Dropped"

    ALL = [
        READING,
        WANT_TO_READ,
        COMPLETED,
        PAUSED,
        DROPPED,
    ]