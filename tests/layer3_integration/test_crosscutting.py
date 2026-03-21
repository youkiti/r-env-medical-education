"""T3-06, T3-07, T3-08: Cross-cutting control tests."""

import subprocess

import pytest

from tests.conftest import PROJECTS_DIR, REPO_ROOT
from tests.helpers.r_script_linter import check_naming_convention


# ── T3-06: Reproducibility standards cross-project ────────────────────


class TestReproducibilityStandards:
    """Validate reproducibility conventions across all projects."""

    @pytest.mark.p1
    def test_script_naming_all_projects(self):
        """All R scripts in all projects must follow naming conventions."""
        if not PROJECTS_DIR.exists():
            pytest.skip("No projects/ directory")

        violations = []
        for project_dir in PROJECTS_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            scripts_dir = project_dir / "scripts"
            if not scripts_dir.exists():
                continue
            for f in scripts_dir.glob("*.R"):
                if not check_naming_convention(f.name):
                    violations.append(f"{project_dir.name}/{f.name}")

        assert not violations, (
            f"Naming convention violations: {violations}"
        )

    @pytest.mark.p1
    def test_figure_pairs_all_projects(self):
        """All figures must have PNG+PDF pairs in all projects."""
        if not PROJECTS_DIR.exists():
            pytest.skip("No projects/ directory")

        violations = []
        for project_dir in PROJECTS_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            figures_dir = project_dir / "output" / "figures"
            if not figures_dir.exists():
                continue
            pngs = {f.stem for f in figures_dir.glob("*.png")}
            pdfs = {f.stem for f in figures_dir.glob("*.pdf")}
            missing_pdf = pngs - pdfs
            missing_png = pdfs - pngs
            if missing_pdf:
                violations.append(f"{project_dir.name}: PNG without PDF: {missing_pdf}")
            if missing_png:
                violations.append(f"{project_dir.name}: PDF without PNG: {missing_png}")

        assert not violations, f"Figure pair violations: {violations}"


# ── T3-07: Privacy gitignore alignment ────────────────────────────────


class TestPrivacyGitignore:
    """Validate .gitignore includes private data paths."""

    @pytest.mark.p0
    def test_gitignore_has_private_patterns(self):
        """.gitignore must include data/private/ pattern."""
        gitignore = REPO_ROOT / ".gitignore"
        if not gitignore.exists():
            pytest.skip(".gitignore not found")
        content = gitignore.read_text(encoding="utf-8")
        assert any(
            "data/private" in line for line in content.split("\n")
        ), ".gitignore must include data/private/"

    @pytest.mark.p0
    def test_no_private_in_git(self):
        """No files under data/private/ should be tracked."""
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        tracked = result.stdout.strip().split("\n") if result.stdout.strip() else []
        private = [
            f for f in tracked
            if "data/private" in f or "data/raw_private" in f
        ]
        assert not private, f"Private data tracked: {private}"


# ── T3-08: Guardrails x TDD enforcement ──────────────────────────────


class TestGuardrailsTDD:
    """utils_*.R must have corresponding test-*.R files."""

    @pytest.mark.p1
    def test_utils_have_tests(self):
        """Every utils_*.R should have a test-*.R counterpart."""
        if not PROJECTS_DIR.exists():
            pytest.skip("No projects/ directory")

        untested = []
        for project_dir in PROJECTS_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            scripts_dir = project_dir / "scripts"
            tests_dir = project_dir / "tests" / "testthat"
            if not scripts_dir.exists():
                continue

            utils_files = list(scripts_dir.glob("utils_*.R"))
            if not utils_files:
                continue

            test_files = (
                {f.name for f in tests_dir.glob("test-*.R")}
                if tests_dir.exists()
                else set()
            )

            for u in utils_files:
                module = u.name.replace("utils_", "").replace(".R", "")
                expected_test = f"test-{module}.R"
                if expected_test not in test_files:
                    untested.append(f"{project_dir.name}/{u.name}")

        if not untested:
            return  # All good or no utils files
        assert not untested, (
            f"utils_*.R without corresponding test-*.R: {untested}"
        )
