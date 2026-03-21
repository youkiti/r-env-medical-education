"""T2-09, T2-10, T2-11, T2-12: Verification artifact validation."""

import json
import pathlib
import re

import pytest
import yaml

from tests.helpers.markdown_parser import extract_table_headers

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


# ── T2-09: verification_config.yml schema ──────────────────────────────


class TestVerificationConfig:
    """Validate verification_config.yml schema."""

    @pytest.fixture(autouse=True)
    def _load(self):
        with open(FIXTURES / "sample_verification_config.yml", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    @pytest.mark.p0
    def test_on_failure_valid(self):
        """on_failure must be 'warn' or 'error'."""
        assert self.config.get("on_failure") in ("warn", "error"), (
            f"on_failure must be 'warn' or 'error', got: {self.config.get('on_failure')}"
        )

    @pytest.mark.p0
    def test_key_results_structure(self):
        """key_results must be an array with id, metric, expected, tolerance."""
        kr = self.config.get("key_results", [])
        assert len(kr) >= 1, "key_results must have at least one entry"
        for item in kr:
            for field in ("id", "metric", "expected", "tolerance"):
                assert field in item, f"key_results entry missing '{field}': {item}"

    @pytest.mark.p0
    def test_key_results_id_format(self):
        """key_results IDs must match G<gate>-<seq> format."""
        pattern = re.compile(r"^G\d+[A-D]?-\d+$")
        for item in self.config.get("key_results", []):
            assert pattern.match(item["id"]), (
                f"Invalid Gate ID in key_results: {item['id']}"
            )

    @pytest.mark.p0
    def test_assumption_checks_structure(self):
        """assumption_checks entries must have required fields."""
        checks = self.config.get("assumption_checks", [])
        if not checks:
            pytest.skip("No assumption_checks defined")
        for item in checks:
            for field in ("id", "model", "check", "required"):
                assert field in item, (
                    f"assumption_checks entry missing '{field}': {item}"
                )


# ── T2-10: qa_inputs.json schema ──────────────────────────────────────


class TestQAInputs:
    """Validate qa_inputs.json schema."""

    @pytest.fixture(autouse=True)
    def _load(self):
        with open(FIXTURES / "sample_qa_inputs.json", encoding="utf-8") as f:
            self.qa = json.load(f)

    @pytest.mark.p0
    def test_key_results_structure(self):
        """key_results must be an array with id, metric, value."""
        kr = self.qa.get("key_results", [])
        assert len(kr) >= 1, "key_results must have at least one entry"
        for item in kr:
            for field in ("id", "metric", "value"):
                assert field in item, f"key_results entry missing '{field}': {item}"

    @pytest.mark.p0
    def test_assumption_checks_structure(self):
        """assumption_checks entries must have all required fields."""
        checks = self.qa.get("assumption_checks", [])
        if not checks:
            pytest.skip("No assumption_checks")
        required_fields = ("id", "model", "check", "required", "result", "status")
        for item in checks:
            for field in required_fields:
                assert field in item, (
                    f"assumption_checks entry missing '{field}': {item}"
                )

    @pytest.mark.p0
    def test_status_values_valid(self):
        """status must be 'pass', 'fail', or 'skipped'."""
        valid = {"pass", "fail", "skipped"}
        for item in self.qa.get("assumption_checks", []):
            assert item["status"] in valid, (
                f"Invalid status '{item['status']}' for check {item['id']}"
            )


# ── T2-11: back_translation.md structure ──────────────────────────────


class TestBackTranslation:
    """Validate back_translation.md structure."""

    @pytest.mark.p1
    def test_has_gate_ids(self):
        """Back translation must reference Gate IDs."""
        text = (FIXTURES / "sample_back_translation.md").read_text(encoding="utf-8")
        ids = re.findall(r"G\d+[A-D]?-\d+", text)
        assert len(ids) >= 1, "Back translation must contain Gate ID references"

    @pytest.mark.p1
    def test_has_description_sections(self):
        """Each Gate ID should have an accompanying description."""
        text = (FIXTURES / "sample_back_translation.md").read_text(encoding="utf-8")
        from tests.helpers.markdown_parser import extract_headings
        headings = extract_headings(text, level=2)
        # Each heading should reference a Gate ID
        ids_in_headings = [h for h in headings if re.search(r"G\d+[A-D]?-\d+", h)]
        assert len(ids_in_headings) >= 1, (
            "Back translation headings should reference Gate IDs"
        )


# ── T2-12: traceability_matrix.md structure ───────────────────────────


class TestTraceabilityMatrix:
    """Validate traceability_matrix.md structure."""

    @pytest.mark.p1
    def test_has_markdown_table(self):
        """Must contain at least one markdown table."""
        text = (FIXTURES / "sample_traceability_matrix.md").read_text(encoding="utf-8")
        tables = extract_table_headers(text)
        assert len(tables) >= 1, "Traceability matrix must contain a markdown table"

    @pytest.mark.p1
    def test_required_columns(self):
        """Table must have 5 required columns."""
        text = (FIXTURES / "sample_traceability_matrix.md").read_text(encoding="utf-8")
        tables = extract_table_headers(text)
        assert len(tables) >= 1
        headers = tables[0]
        required = ["Plan ID", "Plan Description", "Script", "Line Range", "Status"]
        for col in required:
            assert any(col in h for h in headers), (
                f"Missing required column: {col}. Found: {headers}"
            )

    @pytest.mark.p1
    def test_status_values(self):
        """Status column should use valid values."""
        text = (FIXTURES / "sample_traceability_matrix.md").read_text(encoding="utf-8")
        valid_statuses = {"Implemented", "Partial", "Missing"}
        # Extract status column values from table rows
        lines = text.strip().split("\n")
        for line in lines:
            if "|" in line and not line.strip().startswith("|--"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 5 and cells[4] in valid_statuses:
                    continue
                elif len(cells) >= 5 and cells[0] != "Plan ID":
                    assert cells[4] in valid_statuses, (
                        f"Invalid status: '{cells[4]}'. Must be one of {valid_statuses}"
                    )
