"""T4-01 to T4-04: End-to-end smoke tests for chatgpt_diagnostic_study."""

import csv
import pathlib
import subprocess

import pytest

from tests.conftest import PROJECTS_DIR

PROJECT = PROJECTS_DIR / "chatgpt_diagnostic_study"


# ── T4-01: Synthetic data generation script execution ─────────────────


class TestSyntheticDataGeneration:
    """Test 00_generate_synthetic_data.R execution."""

    @pytest.mark.p0
    @pytest.mark.requires_r
    def test_script_runs_successfully(self):
        """Script should exit with code 0."""
        script = PROJECT / "scripts" / "00_generate_synthetic_data.R"
        if not script.exists():
            pytest.skip("00_generate_synthetic_data.R not found")

        result = subprocess.run(
            ["Rscript", str(script)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT),
            timeout=120,
        )
        assert result.returncode == 0, (
            f"Script failed with code {result.returncode}.\n"
            f"stderr: {result.stderr[:500]}"
        )

    @pytest.mark.p0
    @pytest.mark.requires_r
    def test_chatgpt_cases_output(self):
        """Should produce chatgpt_cases_cleaned.csv with 150 rows."""
        csv_path = PROJECT / "data" / "processed" / "chatgpt_cases_cleaned.csv"
        if not csv_path.exists():
            pytest.skip("CSV not generated yet")
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        # First row is header
        assert len(rows) == 151, f"Expected 151 rows (header+150), got {len(rows)}"

    @pytest.mark.p0
    @pytest.mark.requires_r
    def test_diagnostic_accuracy_output(self):
        """Should produce diagnostic_accuracy_600.csv with 600 rows."""
        csv_path = PROJECT / "data" / "processed" / "diagnostic_accuracy_600.csv"
        if not csv_path.exists():
            pytest.skip("CSV not generated yet")
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) == 601, f"Expected 601 rows (header+600), got {len(rows)}"

    @pytest.mark.p0
    @pytest.mark.requires_r
    def test_all_reviews_output(self):
        """Should produce all_reviews.csv with ~300 rows."""
        csv_path = PROJECT / "data" / "processed" / "all_reviews.csv"
        if not csv_path.exists():
            pytest.skip("CSV not generated yet")
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        # Allow some flexibility on exact count
        assert 250 < len(rows) <= 350, (
            f"Expected ~301 rows (header+300), got {len(rows)}"
        )


# ── T4-02: Artifact completeness check ───────────────────────────────

EXPECTED_FILES = {
    # Existing (should pass)
    "data/processed/chatgpt_cases_cleaned.csv": True,
    "data/processed/diagnostic_accuracy_600.csv": True,
    "data/processed/all_reviews.csv": True,
    "README.md": True,
    "output/figures": True,
    "output/tables": True,
    # Missing by design (student project)
    "scripts/00_setup.R": False,
    "scripts/_project_config.R": False,
    "scripts/run_all.R": False,
    "analysis_plan.md": False,
    "verification_config.yml": False,
    "docs/statistical_analysis_plan.md": False,
    "output/verification/back_translation.md": False,
    "output/verification/traceability_matrix.md": False,
    "output/verification/qa_report.md": False,
}


class TestArtifactCompleteness:
    """Check overall project artifact completeness."""

    @pytest.mark.p0
    @pytest.mark.parametrize("relpath,should_exist", [
        (k, v) for k, v in EXPECTED_FILES.items() if v is True
    ])
    def test_existing_artifacts(self, relpath, should_exist):
        """Artifacts expected to exist should be present."""
        path = PROJECT / relpath
        assert path.exists(), f"Expected artifact missing: {relpath}"

    @pytest.mark.p0
    @pytest.mark.parametrize("relpath,should_exist", [
        (k, v) for k, v in EXPECTED_FILES.items() if v is False
    ])
    def test_future_artifacts_documented(self, relpath, should_exist):
        """Document which expected artifacts are not yet created."""
        path = PROJECT / relpath
        # This is informational - these are expected to be missing
        # in the current teaching project state
        if path.exists():
            # If it exists, that's a bonus
            pass
        # No assertion - just documentation


# ── T4-03: Figure PNG/PDF pair completeness ───────────────────────────


class TestFigurePairs:
    """Verify fig1-fig5 PNG/PDF pairs."""

    @pytest.mark.p1
    def test_all_figure_pairs_present(self):
        """fig1 through fig5 should have both PNG and PDF."""
        figures_dir = PROJECT / "output" / "figures"
        if not figures_dir.exists():
            pytest.skip("output/figures/ not found")

        expected_stems = {
            "fig1_percent_correct",
            "fig2_confusion_matrix",
            "fig3_roc_curve",
            "fig4_cognitive_load",
            "fig5_quality_answers",
        }

        pngs = {f.stem for f in figures_dir.glob("*.png")}
        pdfs = {f.stem for f in figures_dir.glob("*.pdf")}

        for stem in expected_stems:
            assert stem in pngs, f"Missing PNG: {stem}.png"
            assert stem in pdfs, f"Missing PDF: {stem}.pdf"


# ── T4-04: run_all.R pipeline (future) ───────────────────────────────


class TestRunAllPipeline:
    """Test full pipeline execution via run_all.R."""

    @pytest.mark.p2
    @pytest.mark.requires_r
    def test_run_all_generates_qa_inputs(self):
        """run_all.R should generate qa_inputs.json (when project is complete)."""
        run_all = PROJECT / "scripts" / "run_all.R"
        if not run_all.exists():
            pytest.skip("run_all.R not yet created (project incomplete)")

        qa_json = PROJECT / "output" / "verification" / "qa_inputs.json"
        result = subprocess.run(
            ["Rscript", str(run_all)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT),
            timeout=300,
        )
        assert result.returncode == 0, f"run_all.R failed: {result.stderr[:500]}"
        assert qa_json.exists(), "qa_inputs.json not generated"
