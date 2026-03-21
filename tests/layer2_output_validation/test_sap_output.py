"""T2-02, T2-03: SAP and checklist structural validation."""

import pathlib

import pytest

from tests.helpers.markdown_parser import extract_checkboxes, extract_headings

FIXTURES = pathlib.Path(__file__).parent / "fixtures"

# ── T2-02: SAP 16 canonical sections ──────────────────────────────────

SAP_REQUIRED_SECTIONS = [
    "Document control",
    "Background",
    "Objectives and hypotheses",
    "Study design and data source",
    "Study population",
    "Variables",
    "Data processing plan",
    "Statistical principles",
    "Descriptive and exploratory analyses",
    "Primary analysis",
    "Secondary analyses",
    "Subgroup analyses",
    "Sensitivity analyses",
    "Reproducibility and code operations",
    "References",
    "Decision log",
]


class TestSAPStructure:
    """Validate SAP structural requirements."""

    @pytest.mark.p0
    def test_has_all_16_sections(self):
        """SAP must contain all 16 canonical sections."""
        text = (FIXTURES / "sample_sap.md").read_text(encoding="utf-8")
        headings = extract_headings(text, level=2)

        missing = []
        for req in SAP_REQUIRED_SECTIONS:
            if not any(req in h for h in headings):
                missing.append(req)

        assert not missing, (
            f"SAP missing sections: {missing}. Found: {headings}"
        )

    @pytest.mark.p0
    def test_sections_in_order(self):
        """SAP sections should appear in canonical order."""
        text = (FIXTURES / "sample_sap.md").read_text(encoding="utf-8")
        headings = extract_headings(text, level=2)

        # Find positions of required sections in actual heading list
        positions = []
        for req in SAP_REQUIRED_SECTIONS:
            for i, h in enumerate(headings):
                if req in h:
                    positions.append(i)
                    break

        # Positions should be monotonically increasing
        for i in range(1, len(positions)):
            assert positions[i] > positions[i - 1], (
                f"Section '{SAP_REQUIRED_SECTIONS[i]}' appears before "
                f"'{SAP_REQUIRED_SECTIONS[i - 1]}' in SAP"
            )


# ── T2-03: Code review checklist ──────────────────────────────────────


class TestChecklist:
    """Validate code_review_checklist.md."""

    @pytest.mark.p1
    def test_has_checkboxes(self):
        """Checklist must contain at least one checkbox item."""
        text = (FIXTURES / "sample_code_review_checklist.md").read_text(encoding="utf-8")
        boxes = extract_checkboxes(text)
        assert len(boxes) >= 1, "Checklist must have at least one checkbox"

    @pytest.mark.p1
    def test_has_multiple_categories(self):
        """Checklist should have categorized sections."""
        text = (FIXTURES / "sample_code_review_checklist.md").read_text(encoding="utf-8")
        headings = extract_headings(text, level=2)
        assert len(headings) >= 2, (
            f"Checklist should have >= 2 category sections, found {len(headings)}"
        )
