from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)

class Toolbar(QWidget):

    def __init__(self):

        super().__init__()

        self.layout = QHBoxLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.layout.setSpacing(
            8
        )

        self.setLayout(
            self.layout
        )

    def add_widget(
        self,
        widget,
        stretch=0,
        alignment=None,
    ):

        if alignment is None:

            self.layout.addWidget(
                widget,
                stretch,
            )

        else:

            self.layout.addWidget(
                widget,
                stretch,
                alignment,
            )

    def add_stretch(self):

        self.layout.addStretch()

    def add_spacing(
        self,
        width: int,
    ):

        self.layout.addSpacerItem(

            QSpacerItem(
                width,
                0,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Minimum,
            )

        )