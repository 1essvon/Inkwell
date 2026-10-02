"""PyInstaller one-folder build for the Inkwell desktop application."""

from pathlib import Path
import os
import sys


ROOT = Path(SPECPATH).resolve()
sys.path.insert(0, str(ROOT))

version_info_file = os.environ.get("INKWELL_VERSION_INFO")
if sys.platform == "win32":
    if not version_info_file or not Path(version_info_file).is_file():
        raise FileNotFoundError(
            "Windows builds require the version resource generated from VERSION."
        )
elif version_info_file is not None:
    raise RuntimeError("INKWELL_VERSION_INFO is only supported for Windows builds.")

from app.styles.load_styles import BASE_STYLE_FILES, THEME_STYLE_FILES

STYLE_FILES = [*BASE_STYLE_FILES, *THEME_STYLE_FILES.values()]


datas = []
styles_directory = ROOT / "app" / "styles"
for filename in STYLE_FILES:
    stylesheet = styles_directory / filename
    if not stylesheet.is_file():
        raise FileNotFoundError(f"Required stylesheet is missing: {stylesheet}")
    datas.append((str(stylesheet), "app/styles"))

alembic_config = ROOT / "alembic.ini"
alembic_environment = ROOT / "alembic" / "env.py"
active_revisions = sorted((ROOT / "alembic" / "versions").glob("*.py"))
for required_file in (alembic_config, alembic_environment):
    if not required_file.is_file():
        raise FileNotFoundError(f"Required Alembic runtime file is missing: {required_file}")
if not active_revisions:
    raise FileNotFoundError("No active Alembic revisions were found.")

datas.extend(
    [
        (str(alembic_config), "."),
        (str(alembic_environment), "alembic"),
    ]
)
datas.extend(
    (str(revision), "alembic/versions")
    for revision in active_revisions
)

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    # The pinned PyInstaller Qt hooks collect Qt Multimedia backend plugins;
    # keep the module explicit because playback is a runtime-only feature.
    hiddenimports=["PySide6.QtMultimedia"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TheInkwell",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    version=version_info_file,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="TheInkwell",
)
