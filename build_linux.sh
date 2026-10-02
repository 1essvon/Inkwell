#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"
APPIMAGETOOL="${APPIMAGETOOL:-appimagetool}"
SPEC_PATH="$ROOT/TheInkwell.spec"
BUILD_REQUIREMENTS="$ROOT/requirements-build-linux.txt"
WORK_PATH="$ROOT/build/linux"
DIST_PATH="$ROOT/dist/linux"
APPLICATION_PATH="$DIST_PATH/TheInkwell/TheInkwell"
APPDIR="$(mktemp -d "${TMPDIR:-/tmp}/inkwell-appdir.XXXXXX")"
TEMP_OUTPUT="$DIST_PATH/.TheInkwell.AppImage.$$"

cleanup() {
    rm -rf -- "$APPDIR"
    if [[ -e "$TEMP_OUTPUT" ]]; then
        rm -f -- "$TEMP_OUTPUT"
    fi
}
trap cleanup EXIT

if [[ "$(uname -s)" != "Linux" ]]; then
    printf 'Linux build must run on Linux; PyInstaller does not cross-compile.\n' >&2
    exit 1
fi

case "$(uname -m)" in
    x86_64)
        ARCH=x86_64
        ;;
    aarch64)
        ARCH=aarch64
        ;;
    *)
        printf 'Unsupported Linux build architecture: %s\n' "$(uname -m)" >&2
        exit 1
        ;;
esac

if [[ ! -f "$SPEC_PATH" || ! -f "$BUILD_REQUIREMENTS" ]]; then
    printf 'The PyInstaller spec or Linux build requirements are missing.\n' >&2
    exit 1
fi

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    printf 'Python interpreter not found: %s\n' "$PYTHON" >&2
    exit 1
fi

if ! "$PYTHON" -c \
    "from importlib.metadata import version; assert version('PyInstaller') == '6.22.3'; assert version('pyinstaller-hooks-contrib') == '2026.7'"
then
    printf 'Install requirements.txt and requirements-build-linux.txt before building.\n' >&2
    exit 1
fi

if ! command -v "$APPIMAGETOOL" >/dev/null 2>&1 && [[ ! -x "$APPIMAGETOOL" ]]; then
    printf 'appimagetool was not found. Install it or set APPIMAGETOOL to its executable path.\n' >&2
    exit 1
fi

mkdir -p -- "$DIST_PATH"
"$PYTHON" -m PyInstaller --noconfirm --clean \
    --distpath "$DIST_PATH" \
    --workpath "$WORK_PATH" \
    "$SPEC_PATH"

if [[ ! -x "$APPLICATION_PATH" ]]; then
    printf 'PyInstaller completed without the expected executable: %s\n' "$APPLICATION_PATH" >&2
    exit 1
fi

mkdir -p -- "$APPDIR/usr/bin"
cp -a -- "$DIST_PATH/TheInkwell" "$APPDIR/usr/bin/"
cp -- "$ROOT/packaging/linux/AppRun" "$APPDIR/AppRun"
cp -- "$ROOT/packaging/linux/TheInkwell.desktop" "$APPDIR/TheInkwell.desktop"
cp -- "$ROOT/packaging/linux/TheInkwell.svg" "$APPDIR/TheInkwell.svg"
chmod +x "$APPDIR/AppRun"

ARCH="$ARCH" "$APPIMAGETOOL" "$APPDIR" "$TEMP_OUTPUT"
if [[ ! -s "$TEMP_OUTPUT" ]]; then
    printf 'appimagetool completed without creating an AppImage.\n' >&2
    exit 1
fi

chmod +x "$TEMP_OUTPUT"
mv -f -- "$TEMP_OUTPUT" "$DIST_PATH/TheInkwell.AppImage"
printf 'Linux application bundle created: %s\n' "$DIST_PATH/TheInkwell.AppImage"
