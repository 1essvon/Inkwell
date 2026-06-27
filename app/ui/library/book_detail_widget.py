"""
File:
    book_detail_widget.py

Purpose:
    Menampilkan detail buku yang sedang dipilih.

Responsibilities:
    - Menampilkan informasi buku
    - Update tampilan
    - Membersihkan tampilan

Does NOT:
    - Mengakses database
    - Membuka dialog
    - Mengubah data buku
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)


class BookDetailWidget(QWidget):
    """
    Widget yang menampilkan detail buku.
    """

    def __init__(self):
        """
        Dipanggil sekali
        saat widget dibuat.
        """

        super().__init__()

        self.setup_ui()

        self.clear()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):
        """
        Membuat seluruh widget.
        """

        self.layout = QVBoxLayout()

        self.title = QLabel()

        self.title.setObjectName(
            "pageTitle"
        )

        self.author = QLabel()

        self.isbn = QLabel()

        self.publisher = QLabel()

        self.genre = QLabel()

        self.status = QLabel()

        self.current_page = QLabel()

        self.rating = QLabel()

        self.layout.addWidget(self.title)

        self.layout.addWidget(self.author)

        self.layout.addWidget(self.isbn)

        self.layout.addWidget(self.publisher)

        self.layout.addWidget(self.genre)

        self.layout.addWidget(self.status)

        self.layout.addWidget(self.current_page)

        self.layout.addWidget(self.rating)

        self.layout.addStretch()

        self.setLayout(
            self.layout
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def clear(self):
        """
        Menampilkan placeholder
        saat belum ada buku dipilih.
        """

        self.title.setText(
            "No Book Selected"
        )

        self.author.clear()

        self.isbn.clear()

        self.publisher.clear()

        self.genre.clear()

        self.status.clear()

        self.current_page.clear()

        self.rating.clear()

    def set_book(
        self,
        book
    ):
        """
        Menampilkan detail buku.
        """

        if book is None:

            self.clear()

            return

        self.title.setText(
            book.title
        )

        self.author.setText(
            f"Author : {book.author}"
        )

        self.isbn.setText(
            f"ISBN : {book.isbn or '-'}"
        )

        self.publisher.setText(
            f"Publisher : {book.publisher or '-'}"
        )

        self.genre.setText(
            f"Genre : {book.genre or '-'}"
        )

        self.status.setText(
            f"Status : {book.status}"
        )

        self.current_page.setText(
            f"Current Page : {book.current_page}"
        )

        self.rating.setText(
            f"Rating : {book.rating or '-'}"
        )