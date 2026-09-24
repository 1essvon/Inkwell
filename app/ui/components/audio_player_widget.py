from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from app.services.audio_service import AudioService
from app.ui.components.base_card import BaseCard


class AudioPlayerWidget(BaseCard):
    """Reusable local audio controls backed by AudioService."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.audio_service = AudioService(self)
        self.audio_path = None
        self._playback_state = "stopped"

        self.layout.setContentsMargins(14, 12, 14, 12)
        self.layout.setSpacing(8)

        self._setup_audio_controls()
        self._connect_audio_signals()
        self.audio_service.set_volume(
            self.volume_slider.value() / 100
        )

    def _setup_audio_controls(self):
        title = QLabel("Reading Audio")
        title.setObjectName("cardTitle")
        self.layout.addWidget(title)

        file_row = QHBoxLayout()
        self.file_label = QLabel(
            "No audio selected. Choose a local file to play."
        )
        self.file_label.setObjectName("secondaryText")
        self.file_label.setMinimumWidth(0)
        self.file_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.choose_button = QPushButton("Choose Audio")
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(self.choose_button)
        self.layout.addLayout(file_row)

        control_row = QHBoxLayout()
        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.setEnabled(False)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        control_row.addWidget(self.play_pause_button)
        control_row.addWidget(self.stop_button)
        self.layout.addLayout(control_row)

        progress_row = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setTextVisible(False)
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("secondaryText")
        progress_row.addWidget(self.progress_bar, 1)
        progress_row.addWidget(self.time_label)
        self.layout.addLayout(progress_row)

        volume_row = QHBoxLayout()
        volume_label = QLabel("Volume")
        volume_label.setObjectName("secondaryText")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(60)
        self.volume_slider.setEnabled(False)
        volume_row.addWidget(volume_label)
        volume_row.addWidget(self.volume_slider, 1)
        self.layout.addLayout(volume_row)

        self.error_label = QLabel()
        self.error_label.setObjectName("audioError")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        self.layout.addWidget(self.error_label)

    def _connect_audio_signals(self):
        self.choose_button.clicked.connect(self.choose_audio_file)
        self.play_pause_button.clicked.connect(self.toggle_playback)
        self.stop_button.clicked.connect(self.stop_playback)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.audio_service.playback_state_changed.connect(
            self._on_playback_state_changed
        )
        self.audio_service.position_changed.connect(
            self._on_position_changed
        )
        self.audio_service.duration_changed.connect(
            self._on_duration_changed
        )
        self.audio_service.error_occurred.connect(
            self._on_error
        )

    def choose_audio_file(self):
        path, _selected_filter = QFileDialog.getOpenFileName(
            self,
            "Choose audio file",
            "",
            "Audio files (*.mp3 *.wav *.ogg *.flac *.m4a *.aac);;All files (*)",
        )

        if not path:
            return

        self.audio_service.stop()
        self.audio_path = Path(path)
        self.file_label.setText(self.audio_path.name)
        self.file_label.setToolTip(str(self.audio_path))
        self.play_pause_button.setEnabled(True)
        self.volume_slider.setEnabled(True)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self._clear_error()

    def toggle_playback(self):
        if self._playback_state == "playing":
            self.audio_service.pause()
        elif self._playback_state == "paused":
            self.audio_service.resume()
        elif self.audio_path is not None:
            self._clear_error()
            self.audio_service.play(self.audio_path)

    def stop_playback(self):
        self.audio_service.stop()
        self._on_position_changed(0)

    def set_volume(self, value):
        self.audio_service.set_volume(value / 100)

    def _on_playback_state_changed(self, state):
        state_name = getattr(state, "name", str(state)).lower()

        if "playing" in state_name:
            self._playback_state = "playing"
            self.play_pause_button.setText("Pause")
            self.stop_button.setEnabled(True)
        elif "paused" in state_name:
            self._playback_state = "paused"
            self.play_pause_button.setText("Resume")
            self.stop_button.setEnabled(True)
        else:
            self._playback_state = "stopped"
            self.play_pause_button.setText("Play")
            self.stop_button.setEnabled(False)

    def _on_position_changed(self, position):
        duration = self.audio_service.duration
        self.progress_bar.setRange(0, max(duration, 1))
        self.progress_bar.setValue(
            min(position, max(duration, 1))
        )
        self._update_time_label(position, duration)

    def _on_duration_changed(self, duration):
        self.progress_bar.setRange(0, max(duration, 1))
        self._update_time_label(
            self.audio_service.position,
            duration,
        )

    def _update_time_label(self, position, duration):
        self.time_label.setText(
            f"{self._format_time(position)} / "
            f"{self._format_time(duration)}"
        )

    @staticmethod
    def _format_time(milliseconds):
        seconds = max(0, milliseconds // 1000)
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def _on_error(self, message):
        self.error_label.setText(message or "Audio playback failed.")
        self.error_label.show()

    def _clear_error(self):
        self.error_label.clear()
        self.error_label.hide()
