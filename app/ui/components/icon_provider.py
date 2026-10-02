"""Small, consistent monochrome vector icons for the application UI."""

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QAbstractButton, QApplication


# Standard icon size hierarchy across the application:
SIZE_NAV = 18       # Sidebar navigation buttons
SIZE_ACTION = 24    # Quick actions buttons
SIZE_INLINE = 16    # Toolbars, inline buttons, status rows
SIZE_DISPLAY = 40   # Empty state illustrations


_ICON_PATHS = {
    "dashboard": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="11" width="7" height="10" rx="1"/><rect x="3" y="14" width="8" height="7" rx="1"/>',
    "library": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21z"/><path d="M4 5.5v13A2.5 2.5 0 0 1 6.5 16H20M8 7h8M8 10h8"/>',
    "reading": '<path d="M12 6.5C9.5 4.5 6 4 3 5v14c3-1 6.5-.5 9 1.5 2.5-2 6-2.5 9-1.5V5c-3-1-6.5-.5-9 1.5z"/><path d="M12 6.5v14M6 8v3M18 8v3"/>',
    "journal": '<path d="M6 3h12a2 2 0 0 1 2 2v16H6a3 3 0 0 1-3-3V6a3 3 0 0 1 3-3z"/><path d="M7 3v15a3 3 0 0 0 3 3M10 8h6M10 12h6M10 16h4"/>',
    "statistics": '<path d="M4 20V11h4v9M10 20V4h4v16M16 20v-8h4v8M3 21h18"/>',
    "focus": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6M12 2v3M19 6l1.5-1.5"/>',
    "history": '<path d="M3 12a9 9 0 1 0 2.6-6.4L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="m19.4 15 .1.1 1.4 1.1-1.4 2.4-1.7-.7a8 8 0 0 1-1.6.9l-.3 1.8h-2.8l-.3-1.8a8 8 0 0 1-1.6-.9l-1.7.7-1.4-2.4 1.4-1.1a8 8 0 0 1 0-1.9l-1.4-1.1 1.4-2.4 1.7.7a8 8 0 0 1 1.6-.9l.3-1.8h2.8l.3 1.8a8 8 0 0 1 1.6.9l1.7-.7 1.4 2.4-1.4 1.1a8 8 0 0 1-.1 1.9z" transform="translate(-1 -1)"/>',
    "add_book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H17v16H6.5A2.5 2.5 0 0 0 4 21z"/><path d="M7 8h6M7 11h6M19 7v7M15.5 10.5h7"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z"/>',
    "note": '<path d="M5 3h14v18H5zM8 7h8M8 11h8M8 15h5"/><path d="M17 3v4h2"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M6 6h10M6 10h10"/>',
    "quote": '<path d="M3 13h4a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v4a6 6 0 0 0 6 6M15 13h4a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4a6 6 0 0 0 6 6"/>',
    "bookmark": '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "pause": '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
    "cross": '<path d="M18 6 6 18M6 6l12 12"/>',
}


def has_icon(name: str) -> bool:
    """Check if an icon name is registered in the provider."""
    return name in _ICON_PATHS


def _get_active_color(color: str | None = None) -> str:
    """Resolve the active theme icon color or fallback."""
    if color is not None:
        return color
    application = QApplication.instance()
    resolved = (
        application.property("inkwell_icon_color")
        if application is not None
        else None
    )
    return resolved or "#111111"


def pixmap(name: str, size: int = 20, color: str | None = None) -> QPixmap:
    """Render a 24px stroke SVG as a QPixmap at the requested size."""
    if name not in _ICON_PATHS:
        raise KeyError(f"Unknown icon '{name}'")

    stroke_color = _get_active_color(color)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        f'viewBox="0 0 24 24" fill="none" stroke="{stroke_color}" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f"{_ICON_PATHS[name]}</svg>"
    )
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    px = QPixmap(QSize(size, size))
    px.fill(Qt.GlobalColor.transparent)
    painter = QPainter(px)
    renderer.render(painter)
    painter.end()
    return px


def icon(name: str, size: int = 20, color: str | None = None) -> QIcon:
    """Render a 24px stroke SVG as a QIcon at the requested size."""
    return QIcon(pixmap(name, size=size, color=color))


def set_button_icon(
    button: QAbstractButton,
    name: str,
    size: int = SIZE_NAV,
    color: str | None = None,
) -> None:
    """Convenience helper to set a theme-aware icon on a button consistently."""
    button.setProperty("inkwell_icon_name", name)
    button.setIcon(icon(name, size=size, color=color))
    button.setIconSize(QSize(size, size))

