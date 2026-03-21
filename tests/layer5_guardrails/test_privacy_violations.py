"""T5-03, T5-04: Privacy violation detection tests."""

import pathlib
import re
import subprocess

import pytest

from tests.conftest import REPO_ROOT

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


# ── T5-04: Detect private data paths tracked by git ───────────────────


class TestGitPrivateData:
    """Ensure private data directories are not tracked by git."""

    @pytest.mark.p0
    def test_gitignore_has_data_private(self):
        """'.gitignore' must include data/private/ pattern."""
        gitignore = REPO_ROOT / ".gitignore"
        if not gitignore.exists():
            pytest.skip(".gitignore not found")
        content = gitignore.read_text(encoding="utf-8")
        assert any(
            "data/private" in line
            for line in content.split("\n")
        ), ".gitignore must include data/private/ pattern"

    @pytest.mark.p0
    def test_no_private_files_tracked(self):
        """No files under data/private/ should be tracked by git."""
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        tracked = result.stdout.strip().split("\n")
        private_files = [
            f for f in tracked
            if f.startswith("data/private/") or f.startswith("data/raw_private/")
        ]
        assert not private_files, (
            f"Private data files tracked by git: {private_files}"
        )


# ── T5-03: Detect sensitive data in output artifacts ──────────────────


class TestSensitiveDataInOutput:
    """Detect personal identifiers or private paths in outputs."""

    SENSITIVE_PATTERNS = [
        r"data/private/",
        r"data/raw_private/",
        r"\bPatient\s+ID\s+\d+",
        r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\s*\(case\s+\d+\)",
    ]

    @pytest.mark.p0
    def test_bad_output_detected(self):
        """Verification artifact with sensitive data should be flagged."""
        text = (FIXTURES / "bad_sensitive_output.md").read_text(encoding="utf-8")
        found = []
        for pattern in self.SENSITIVE_PATTERNS:
            if re.search(pattern, text):
                found.append(pattern)
        assert len(found) > 0, "Should detect sensitive data patterns"

    @pytest.mark.p0
    def test_clean_output_passes(self):
        """Normal verification artifact should not be flagged."""
        # Use a clean fixture from layer2
        clean = FIXTURES.parent.parent / "layer2_output_validation" / "fixtures" / "sample_back_translation.md"
        text = clean.read_text(encoding="utf-8")
        found = []
        for pattern in self.SENSITIVE_PATTERNS:
            if re.search(pattern, text):
                found.append(pattern)
        assert len(found) == 0, f"False positive sensitive patterns: {found}"
