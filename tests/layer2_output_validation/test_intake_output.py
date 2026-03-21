"""T2-01, T2-16: Intake summary and cleaning log structural validation."""

import pathlib

import pytest

from tests.helpers.markdown_parser import extract_headings

FIXTURES = pathlib.Path(__file__).parent / "fixtures"

# ── T2-01: intake_summary.md structural validation ────────────────────

INTAKE_REQUIRED_SECTIONS = [
    "Study Goal",
    "Design",
    "Outcome and Exposure",
    "Variables and Coding",
    "Missingness",
    "Reporting Needs",
    "Additional Planning Inputs",
    "Open Questions",
]


class TestIntakeSummary:
    """Validate intake_summary.md structure."""

    @pytest.mark.p0
    def test_has_all_required_sections(self):
        """intake_summary.md must contain all 8 required sections."""
        text = (FIXTURES / "sample_intake_summary.md").read_text(encoding="utf-8")
        headings = extract_headings(text, level=2)

        missing = []
        for req in INTAKE_REQUIRED_SECTIONS:
            if not any(req in h for h in headings):
                missing.append(req)

        assert not missing, f"Missing intake sections: {missing}"

    @pytest.mark.p0
    def test_open_questions_not_empty(self):
        """Open Questions section must have content."""
        text = (FIXTURES / "sample_intake_summary.md").read_text(encoding="utf-8")
        # Find Open Questions section and check it has content
        import re
        match = re.search(
            r"## Open Questions\s*\n(.*?)(?=\n## |\Z)",
            text,
            re.DOTALL,
        )
        assert match, "Open Questions section not found"
        content = match.group(1).strip()
        assert len(content) > 10, "Open Questions section appears empty"


# ── T2-16: Cleaning log structural validation ─────────────────────────


class TestCleaningLog:
    """Validate cleaning log structure."""

    @pytest.mark.p2
    def test_has_row_counts(self):
        """Cleaning log must report input and output row counts."""
        text = (FIXTURES / "sample_cleaning_log.md").read_text(encoding="utf-8")
        assert "Input rows" in text or "input rows" in text
        assert "Output rows" in text or "output rows" in text

    @pytest.mark.p2
    def test_has_exclusions(self):
        """Cleaning log must document exclusion criteria."""
        text = (FIXTURES / "sample_cleaning_log.md").read_text(encoding="utf-8")
        assert "Exclusion" in text or "exclusion" in text or "Removed" in text

    @pytest.mark.p2
    def test_has_type_conversions(self):
        """Cleaning log must document type conversions."""
        text = (FIXTURES / "sample_cleaning_log.md").read_text(encoding="utf-8")
        assert "Type" in text or "type" in text or "conversion" in text.lower()
