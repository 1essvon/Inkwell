from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_windows_installer_uses_valid_canonical_release_version(self):
        version = (REPOSITORY_ROOT / "VERSION").read_text(
            encoding="ascii"
        ).strip()
        windows_build = (REPOSITORY_ROOT / "build_windows.ps1").read_text(
            encoding="utf-8"
        )
        installer = (
            REPOSITORY_ROOT / "packaging" / "windows" / "TheInkwell.iss"
        ).read_text(encoding="utf-8")

        self.assertRegex(version, re.compile(r"^\d+\.\d+\.\d+$"))
        self.assertIn('"VERSION"', windows_build)
        self.assertIn('"/DAppVersion=$ReleaseVersion"', windows_build)
        self.assertIn("AppVersion={#AppVersion}", installer)
        self.assertNotRegex(installer, re.compile(r"^AppVersion=\d", re.MULTILINE))


if __name__ == "__main__":
    unittest.main()
