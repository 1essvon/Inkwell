from pathlib import Path


STYLE_FILES = [

    "00_base.qss",

    "01_typography.qss",

    "02_button.qss",

    "03_input.qss",

    "04_card.qss",

    "05_components.qss",

    "06_progress.qss",

    "07_metrics.qss",

    "08_search.qss",

    "09_empty_state.qss",

    "10_toolbar.qss",

    "11_lists.qss"

]


def load_styles():

    styles_path = Path(__file__).parent

    styles = []

    for filename in STYLE_FILES:

        file = styles_path / filename

        if file.exists():

            styles.append(
                file.read_text(
                    encoding="utf-8"
                )
            )

    return "\n\n".join(styles)