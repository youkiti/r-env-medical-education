"""T2-06, T2-07, T2-08, T2-14, T2-15: R script convention tests."""

import pathlib

import pytest

from tests.conftest import PROJECTS_DIR
from tests.helpers.r_script_linter import (
    check_naming_convention,
    detect_side_effects,
    extract_plan_ids,
)

FIXTURES = pathlib.Path(__file__).parent / "fixtures"
CHATGPT_PROJECT = PROJECTS_DIR / "chatgpt_diagnostic_study"


# ── T2-06: Script naming convention ───────────────────────────────────


class TestScriptNaming:
    """Validate R script naming patterns."""

    @pytest.mark.p1
    @pytest.mark.parametrize("filename,expected", [
        ("00_setup.R", True),
        ("01_import_data.R", True),
        ("utils_clean_data.R", True),
        ("test-clean_data.R", True),
        ("helper-test_data.R", True),
        ("_project_config.R", True),
        ("run_all.R", True),
        ("MyAnalysis.R", False),
        ("analysis script.R", False),
        ("SETUP.R", False),
    ])
    def test_naming_patterns(self, filename, expected):
        """Test naming convention checker against known patterns."""
        assert check_naming_convention(filename) == expected, (
            f"Expected {expected} for '{filename}'"
        )


# ── T2-07: @plan_id tag presence ─────────────────────────────────────


class TestPlanIdTags:
    """Validate @plan_id tags in scripts."""

    @pytest.mark.p1
    def test_extract_plan_ids(self):
        """Should correctly extract @plan_id tags."""
        content = """
# @plan_id G0B-1
import_data()
# @plan_id G1-3
verify_accuracy()
# @plan_id G2B-2
compute_auc()
"""
        ids = extract_plan_ids(content)
        assert ids == ["G0B-1", "G1-3", "G2B-2"]

    @pytest.mark.p1
    def test_no_plan_ids_in_utils(self):
        """utils_*.R should not contain @plan_id tags."""
        # Test with a sample utils file content
        content = """
clean_variable <- function(x) {
    x <- trimws(x)
    x[x == ""] <- NA
    x
}
"""
        ids = extract_plan_ids(content)
        assert len(ids) == 0, "utils_*.R should not have @plan_id tags"


# ── T2-08: Dual figure export (PNG + PDF) ─────────────────────────────


class TestDualFigureExport:
    """Validate PNG/PDF pairs in output/figures/."""

    @pytest.mark.p1
    def test_png_pdf_pairs(self):
        """Every PNG must have a corresponding PDF."""
        figures_dir = CHATGPT_PROJECT / "output" / "figures"
        if not figures_dir.exists():
            pytest.skip("output/figures/ not found")

        pngs = {f.stem for f in figures_dir.glob("*.png")}
        pdfs = {f.stem for f in figures_dir.glob("*.pdf")}

        missing_pdf = pngs - pdfs
        assert not missing_pdf, (
            f"PNG without corresponding PDF: {missing_pdf}"
        )

    @pytest.mark.p1
    def test_pdf_png_pairs(self):
        """Every PDF should have a corresponding PNG."""
        figures_dir = CHATGPT_PROJECT / "output" / "figures"
        if not figures_dir.exists():
            pytest.skip("output/figures/ not found")

        pngs = {f.stem for f in figures_dir.glob("*.png")}
        pdfs = {f.stem for f in figures_dir.glob("*.pdf")}

        missing_png = pdfs - pngs
        assert not missing_png, (
            f"PDF without corresponding PNG: {missing_png}"
        )


# ── T2-14: utils_*.R / test-*.R naming pairs ─────────────────────────


class TestTDDPairs:
    """Validate 1:1 mapping between utils and test files."""

    @pytest.mark.p1
    def test_pair_validation_logic(self):
        """Each utils_<module>.R must have a test-<module>.R."""
        # Test the logic itself with mock data
        utils = {"utils_clean_data.R", "utils_compute.R"}
        tests = {"test-clean_data.R"}

        untested = set()
        for u in utils:
            module = u.replace("utils_", "").replace(".R", "")
            test_name = f"test-{module}.R"
            if test_name not in tests:
                untested.add(u)

        assert untested == {"utils_compute.R"}


# ── T2-15: utils_*.R side-effect-free validation ─────────────────────


class TestUtilsSideEffects:
    """Validate utils_*.R contains no side effects."""

    @pytest.mark.p1
    def test_detect_violations(self):
        """Should detect library(), source(), <<- in utils files."""
        content = """
library(dplyr)
source("config.R")
my_func <- function(x) {
    result <<- x + 1
    result
}
"""
        violations = detect_side_effects(content)
        assert "library()" in violations
        assert "source()" in violations
        assert "<<- assignment" in violations

    @pytest.mark.p1
    def test_clean_utils_passes(self):
        """Pure function definitions should have no violations."""
        content = """
clean_variable <- function(x) {
    x <- trimws(x)
    x[x == ""] <- NA
    x
}

compute_mean <- function(x, na.rm = TRUE) {
    mean(x, na.rm = na.rm)
}
"""
        violations = detect_side_effects(content)
        assert len(violations) == 0, f"Unexpected violations: {violations}"
