from app.services.settings_service import SettingsService
from app.styles.load_styles import load_styles


class ThemeService:
    DEFAULT_THEME = "ink_and_paper"
    THEMES = {
        "white_on_black": {
            "icon": "#F2F2F2",
            "progress_track": "#383838",
            "progress": "#E0E0E0",
            "progress_text": "#F2F2F2",
        },
        "black_on_white": {
            "icon": "#222222",
            "progress_track": "#E6E6E6",
            "progress": "#333333",
            "progress_text": "#111111",
        },
        "ink_and_paper": {
            "icon": "#302B25",
            "progress_track": "#E4DACB",
            "progress": "#8A6242",
            "progress_text": "#302B25",
        },
    }
    LEGACY_THEME_ALIASES = {
        "dark": "black_on_white",
        "monochrome": "black_on_white",
    }

    @staticmethod
    def normalize_theme_name(theme_name):
        if not isinstance(theme_name, str):
            return ThemeService.DEFAULT_THEME

        normalized = theme_name.strip().lower().replace(" ", "_")
        normalized = ThemeService.LEGACY_THEME_ALIASES.get(
            normalized,
            normalized,
        )
        if normalized not in ThemeService.THEMES:
            return ThemeService.DEFAULT_THEME
        return normalized

    @staticmethod
    def get_theme_name():
        settings = SettingsService.get()
        return ThemeService.normalize_theme_name(
            getattr(settings, "theme", None)
        )

    @staticmethod
    def palette_for(theme_name):
        normalized = ThemeService.normalize_theme_name(theme_name)
        return dict(ThemeService.THEMES[normalized])

    @staticmethod
    def load_theme(theme_name=None):
        selected_theme = (
            ThemeService.get_theme_name()
            if theme_name is None
            else ThemeService.normalize_theme_name(theme_name)
        )
        return load_styles(selected_theme)

    @staticmethod
    def apply_theme(app, theme_name=None):
        selected_theme = (
            ThemeService.get_theme_name()
            if theme_name is None
            else ThemeService.normalize_theme_name(theme_name)
        )
        app.setStyleSheet(load_styles(selected_theme))
        app.setProperty("inkwell_theme", selected_theme)

        palette = ThemeService.palette_for(selected_theme)
        app.setProperty("inkwell_icon_color", palette["icon"])
        from app.ui.components.icon_provider import icon
        from app.ui.components.circular_progress import CircularProgress
        from PySide6.QtWidgets import QApplication, QAbstractButton

        for widget in QApplication.allWidgets():
            if isinstance(widget, QAbstractButton):
                icon_name = widget.property("inkwell_icon_name")
                if icon_name:
                    widget.setIcon(
                        icon(
                            icon_name,
                            size=max(1, widget.iconSize().width()),
                            color=palette["icon"],
                        )
                    )

            if isinstance(widget, CircularProgress):
                widget.set_theme_palette(palette)
