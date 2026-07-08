from pathlib import Path


def load_styles():

    style_file = (

        Path(__file__).parent

        / "dark.qss"

    )

    return style_file.read_text(
        encoding="utf-8"
    )