"""T2-05, T2-13: Project skeleton and setup script validation."""

import pathlib
import re

import pytest

from tests.conftest import PROJECTS_DIR

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


# ── T2-05: Project skeleton structure ──────────────────────────────────


class TestProjectSkeleton:
    """Validate project directory structure."""

    @pytest.mark.p0
    @pytest.mark.parametrize("subpath", [
        "README.md",
        "scripts",
        "output/figures",
        "output/tables",
        "output/verification",
    ])
    def test_required_paths_exist(self, subpath):
        """Each project must have required directories and files."""
        project = PROJECTS_DIR / "chatgpt_diagnostic_study"
        path = project / subpath
        assert path.exists(), (
            f"Missing required path: {subpath} in chatgpt_diagnostic_study"
        )

    @pytest.mark.p1
    def test_script_naming_convention(self):
        """All .R files in scripts/ must follow naming conventions."""
        from tests.helpers.r_script_linter import check_naming_convention
        project = PROJECTS_DIR / "chatgpt_diagnostic_study"
        scripts_dir = project / "scripts"
        if not scripts_dir.exists():
            pytest.skip("scripts/ directory not found")
        violations = []
        for f in scripts_dir.glob("*.R"):
            if not check_naming_convention(f.name):
                violations.append(f.name)
        assert not violations, f"Naming convention violations: {violations}"


# ── T2-13: 00_setup.R structural conventions ──────────────────────────


class TestSetupScript:
    """Validate 00_setup.R structure."""

    @pytest.mark.p1
    def test_sources_project_config(self):
        """00_setup.R must source _project_config.R."""
        content = (FIXTURES / "sample_00_setup.R").read_text(encoding="utf-8")
        assert re.search(r'source\(["\']_project_config\.R["\']\)', content), (
            "00_setup.R must source('_project_config.R')"
        )

    @pytest.mark.p1
    def test_records_r_version(self):
        """00_setup.R should record R version."""
        content = (FIXTURES / "sample_00_setup.R").read_text(encoding="utf-8")
        assert "R.version" in content or "R.Version" in content, (
            "00_setup.R should reference R.version"
        )

    @pytest.mark.p1
    def test_uses_requirenamespace(self):
        """00_setup.R should use requireNamespace for package checks."""
        content = (FIXTURES / "sample_00_setup.R").read_text(encoding="utf-8")
        assert "requireNamespace" in content, (
            "00_setup.R should use requireNamespace() for package availability checks"
        )
