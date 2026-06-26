from pathlib import Path


def load_styles():

    style_dir = Path(__file__).parent

    stylesheet = ""

    for file in sorted(style_dir.glob("*.qss")):

        stylesheet += file.read_text(
            encoding="utf-8"
        )

        stylesheet += "\n"

    return stylesheet