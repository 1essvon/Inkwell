APP_STYLESHEET = """

QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    background-color: #1e1e1e;
    color: #f5f5f5;
    font-size: 14px;
    font-family: "Inter", "Segoe UI", sans-serif;
}

QLabel {

    color: #f5f5f5;

    background: transparent;

}

QLabel#pageTitle {
    font-size: 26px;
    font-weight: 700;
}

QLabel#cardTitle {
    font-size: 15px;
    font-weight: 600;
}

QLabel#secondaryText {
    color: #a8a8a8;
}

QLabel#cardValue {
    font-size: 28px;
    font-weight: bold;
}

QLabel#summaryItem {
    color: #c8c8c8;
}

QLabel#pageSubtitle {

    color: #9b9b9b;

    font-size: 13px;

}

QLabel#emptyIcon {

    font-size: 52px;

}

QLabel#emptyTitle {

    font-size: 22px;

    font-weight: bold;

}

QLabel#emptySubtitle {

    color: #9b9b9b;

}

QLabel#badgeReading,
QLabel#badgeFinished,
QLabel#badgeWaiting,
QLabel#badgeDanger,
QLabel#badgeDefault {

    padding: 4px 10px;

    border-radius: 12px;

    font-weight: 600;

}

QLabel#badgeReading {

    background: #2f6feb;

}

QLabel#badgeFinished {

    background: #238636;

}

QLabel#badgeWaiting {

    background: #8b949e;

}

QLabel#badgeDanger {

    background: #da3633;

}

QLabel#badgeDefault {

    background: #444444;

}

QPushButton {

    background-color: #2b2b2b;

    border: 1px solid #404040;

    border-radius: 8px;

    padding: 10px 16px;

    min-height: 18px;
}

QPushButton:hover {

    background-color: #353535;

}

QPushButton:pressed {

    background-color: #454545;

}

QPushButton:disabled {

    background-color: #252525;

    color: #777777;

    border: 1px solid #333333;

}

QListWidget {

    background-color: transparent;

    border: none;

    outline: none;

    padding: 4px;

}

QListWidget::item {

    border: none;

    margin: 4px 0px;

}

QListWidget::item:selected {

    background: transparent;

}

QListWidget::item:hover {

    background: transparent;

}

QLineEdit,
QTextEdit
{

    background-color: #2a2a2a;

    border: 1px solid #3f3f3f;

    border-radius: 8px;

    padding: 8px;
}

QLineEdit:focus,
QTextEdit:focus
 {

    border: 1px solid #5a8dee;

}

QGroupBox {

    border: 1px solid #353535;

    border-radius: 10px;

    margin-top: 12px;

    padding: 12px;

    font-weight: 600;

}

QGroupBox::title {

    subcontrol-origin: margin;

    left: 12px;

    padding: 0px 8px;

}

QProgressBar {

    border: none;

    background-color: #2b2b2b;

    border-radius: 5px;

    min-height: 8px;

    max-height: 8px;

}

QProgressBar::chunk {

    background-color: #5a8dee;

    border-radius: 5px;

}

QScrollArea {

    border: none;

    background: transparent;

}

QScrollArea > QWidget > QWidget {

    background: transparent;

}

QScrollBar:vertical {

    background: transparent;

    width: 10px;

    margin: 0px;

}

QScrollBar::handle:vertical {

    background: #505050;

    border-radius: 5px;

    min-height: 30px;

}

QScrollBar::handle:vertical:hover {

    background: #666666;

}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {

    height: 0px;

}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {

    background: transparent;

}

QScrollBar:horizontal {

    background: transparent;

    height: 10px;

}

QScrollBar::handle:horizontal {

    background: #505050;

    border-radius: 5px;

    min-width: 30px;

}

QScrollBar::handle:horizontal:hover {

    background: #666666;

}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {

    width: 0px;

}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {

    background: transparent;

}

QSplitter::handle {

    background-color: #303030;

}

QSplitter::handle:hover {

    background-color: #4d4d4d;

}

QComboBox {

    background-color: #2b2b2b;

    border: 1px solid #404040;

    border-radius: 8px;

    padding: 8px 12px;

}

QComboBox:hover {

    border: 1px solid #5a5a5a;

}

QComboBox:focus {

    border: 1px solid #5a8dee;

}

QComboBox::drop-down {

    border: none;

    width: 28px;

}

QSpinBox {

    background-color: #2b2b2b;

    border: 1px solid #404040;

    border-radius: 8px;

    padding: 6px 10px;

}

QSpinBox:hover {

    border: 1px solid #5a5a5a;

}

QSpinBox:focus {

    border: 1px solid #5a8dee;

}

QTextEdit {

    background-color: #282828;

    border: 1px solid #3d3d3d;

    border-radius: 8px;

    padding: 10px;

    selection-background-color: #5a8dee;

}

QLineEdit {

    background-color: #282828;

    border: 1px solid #3d3d3d;

    border-radius: 8px;

    padding: 8px 10px;

}

QLineEdit:hover {

    border: 1px solid #555555;

}

QLineEdit:focus {

    border: 1px solid #5a8dee;

}

QDialog {

    background-color: #202020;

}

QMessageBox {

    background-color: #202020;

}

QMessageBox QLabel {

    color: #f5f5f5;

}

QToolTip {

    background-color: #2d2d2d;

    color: white;

    border: 1px solid #5a8dee;

    padding: 6px;

    border-radius: 6px;

}

* {

    selection-background-color: #5a8dee;

    selection-color: white;

}
"""