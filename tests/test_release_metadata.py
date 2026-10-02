from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_release_consumers_use_the_canonical_version(self):
        version = (REPOSITORY_ROOT / "VERSION").read_text(
            encoding="ascii"
        ).strip()
        windows_build = (REPOSITORY_ROOT / "build_windows.ps1").read_text(
            encoding="utf-8"
        )
        pyinstaller_spec = (REPOSITORY_ROOT / "TheInkwell.spec").read_text(
            encoding="utf-8"
        )
        roadmap = (REPOSITORY_ROOT / "DEVELOPMENT_ROADMAP.md").read_text(
            encoding="utf-8"
        )
        installer = (
            REPOSITORY_ROOT / "packaging" / "windows" / "TheInkwell.iss"
        ).read_text(encoding="utf-8")

        self.assertRegex(version, re.compile(r"^\d+\.\d+\.\d+$"))
        self.assertIn(f"**Version:** {version}", roadmap)
        self.assertIn(f"Versi {version} dianggap selesai", roadmap)
        self.assertIn('"VERSION"', windows_build)
        self.assertIn('"/DAppVersion=$ReleaseVersion"', windows_build)
        self.assertIn("$env:INKWELL_VERSION_INFO = $VersionInfoFile", windows_build)
        self.assertIn(
            "Each release version component must be between 0 and 65535",
            windows_build,
        )
        self.assertIn(
            "FixedFileInfo(filevers=__VERSION_TUPLE__, prodvers=__VERSION_TUPLE__)",
            windows_build,
        )
        self.assertIn("FileVersion', '__VERSION__'", windows_build)
        self.assertIn("ProductVersion', '__VERSION__'", windows_build)
        self.assertIn('os.environ.get("INKWELL_VERSION_INFO")', pyinstaller_spec)
        self.assertIn("version=version_info_file", pyinstaller_spec)
        self.assertIn("AppVersion={#AppVersion}", installer)
        self.assertNotRegex(installer, re.compile(r"^AppVersion=\d", re.MULTILINE))


if __name__ == "__main__":
    unittest.main()
