from pathlib import Path


BASE_STYLE_FILES = [

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

    "11_lists.qss",

]

THEME_STYLE_FILES = {
    "black_on_white": "12_black_on_white.qss",
    "white_on_black": "13_white_on_black.qss",
    "ink_and_paper": "12_paper_theme.qss",
}


def load_styles(theme_name="black_on_white"):

    styles_path = Path(__file__).parent

    styles = []

    filenames = [
        *BASE_STYLE_FILES,
        THEME_STYLE_FILES.get(
            theme_name,
            THEME_STYLE_FILES["black_on_white"],
        ),
    ]

    for filename in filenames:

        file = styles_path / filename

        if file.exists():

            styles.append(
                file.read_text(
                    encoding="utf-8"
                )
            )

    return "\n\n".join(styles)
