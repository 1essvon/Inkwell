from pathlib import Path

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class AudioService(QObject):
    """Controls local audio playback for application UI consumers."""

    playback_state_changed = Signal(object)
    position_changed = Signal(int)
    duration_changed = Signal(int)
    error_occurred = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._player = QMediaPlayer(self)
        self._audio_output = QAudioOutput(self)
        self._player.setAudioOutput(self._audio_output)

        self._player.playbackStateChanged.connect(
            self.playback_state_changed
        )
        self._player.positionChanged.connect(
            self.position_changed
        )
        self._player.durationChanged.connect(
            self.duration_changed
        )
        self._player.errorOccurred.connect(
            self._on_error
        )

    @property
    def playback_state(self):
        return self._player.playbackState()

    @property
    def position(self):
        return self._player.position()

    @property
    def duration(self):
        return self._player.duration()

    def play(self, audio_path: str | Path) -> bool:
        try:
            path = Path(audio_path).expanduser()

            if not path.is_file():
                self.error_occurred.emit(
                    f"Audio file not found: {path}"
                )
                return False

        except (OSError, TypeError, ValueError) as error:
            self.error_occurred.emit(
                f"Invalid audio file path: {error}"
            )
            return False

        self._player.setSource(
            QUrl.fromLocalFile(str(path.resolve()))
        )
        self._player.play()
        return True

    def pause(self):
        if self._player.playbackState() == QMediaPlayer.PlayingState:
            self._player.pause()

    def resume(self):
        if self._player.playbackState() == QMediaPlayer.PausedState:
            self._player.play()

    def stop(self):
        self._player.stop()

    def set_volume(self, volume: float):
        self._audio_output.setVolume(
            max(0.0, min(1.0, float(volume)))
        )

    def _on_error(self, _error):
        self.error_occurred.emit(
            self._player.errorString()
        )
