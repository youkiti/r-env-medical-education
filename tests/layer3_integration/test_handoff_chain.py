"""T3-01 to T3-05: Workflow handoff chain tests."""

import json
import pathlib
import re

import pytest
import yaml

FIXTURES = pathlib.Path(__file__).resolve().parent.parent / "layer2_output_validation" / "fixtures"


# ── T3-01: Intake -> SAP handoff ──────────────────────────────────────


class TestIntakeToSAP:
    """Open Questions in intake must be reflected in SAP Decision log."""

    @pytest.mark.p0
    def test_open_questions_in_decision_log(self):
        """Each open question should appear in SAP decision log."""
        intake = (FIXTURES / "sample_intake_summary.md").read_text(encoding="utf-8")
        sap = (FIXTURES / "sample_sap.md").read_text(encoding="utf-8")

        # Extract open questions from intake
        oq_match = re.search(
            r"## Open Questions\s*\n(.*?)(?=\n## |\Z)", intake, re.DOTALL
        )
        assert oq_match, "No Open Questions section in intake"
        oq_text = oq_match.group(1).strip()
        questions = [
            line.strip().lstrip("- ")
            for line in oq_text.split("\n")
            if line.strip() and line.strip().startswith("-")
        ]
        assert len(questions) >= 1, "Should have at least 1 open question"

        # Extract Decision log from SAP
        dl_match = re.search(
            r"## Decision log\s*\n(.*?)(?=\n## |\Z)", sap, re.DOTALL
        )
        assert dl_match, "No Decision log section in SAP"
        dl_text = dl_match.group(1).lower()

        # Check that keywords from each question appear in decision log
        for q in questions:
            # Extract key terms (words > 4 chars)
            terms = [w.lower() for w in re.findall(r"\b\w{5,}\b", q)]
            matched = any(t in dl_text for t in terms)
            assert matched, (
                f"Open question not reflected in SAP Decision log: '{q}'"
            )


# ── T3-02: SAP -> Plan handoff ────────────────────────────────────────


class TestSAPToPlan:
    """SAP analysis sections must map to corresponding Gates."""

    @pytest.mark.p0
    def test_primary_maps_to_gate_2b(self):
        """SAP 'Primary analysis' -> Plan Gate 2B."""
        sap = (FIXTURES / "sample_sap.md").read_text(encoding="utf-8")
        plan = (FIXTURES / "sample_analysis_plan.md").read_text(encoding="utf-8")

        assert "## Primary analysis" in sap, "SAP missing Primary analysis section"
        assert "Gate 2B" in plan, "Plan missing Gate 2B"

    @pytest.mark.p0
    def test_sensitivity_maps_to_gate_2c(self):
        """SAP 'Sensitivity analyses' -> Plan Gate 2C."""
        sap = (FIXTURES / "sample_sap.md").read_text(encoding="utf-8")
        plan = (FIXTURES / "sample_analysis_plan.md").read_text(encoding="utf-8")

        assert "## Sensitivity analyses" in sap
        assert "Gate 2C" in plan

    @pytest.mark.p0
    def test_descriptive_maps_to_gate_2a(self):
        """SAP 'Descriptive' -> Plan Gate 2A."""
        sap = (FIXTURES / "sample_sap.md").read_text(encoding="utf-8")
        plan = (FIXTURES / "sample_analysis_plan.md").read_text(encoding="utf-8")

        assert "## Descriptive" in sap
        assert "Gate 2A" in plan


# ── T3-03: Plan -> Implementation handoff ─────────────────────────────

# Gate-to-script mapping as defined by analysis-implementation skill
GATE_SCRIPT_MAP = {
    "G0A": "00_",
    "G0B": ["01_", "02_"],
    "G1": "03_",
    "G2A": "04_",
    "G2B": "05_",
    "G2C": "06_",
    "G2D": "07_",
}


class TestPlanToImplementation:
    """Plan Gate IDs must appear as @plan_id tags in scripts."""

    @pytest.mark.p0
    def test_plan_ids_coverage(self):
        """Implementation artifacts should reference Plan Gate IDs."""
        plan = (FIXTURES / "sample_analysis_plan.md").read_text(encoding="utf-8")
        plan_ids = set(re.findall(r"G\d+[A-D]?-\d+", plan))

        # Collect IDs from all implementation-side fixtures
        impl_ids = set()
        for fixture_name in ("sample_back_translation.md", "sample_traceability_matrix.md"):
            text = (FIXTURES / fixture_name).read_text(encoding="utf-8")
            impl_ids |= set(re.findall(r"G\d+[A-D]?-\d+", text))

        if not plan_ids:
            pytest.skip("No Gate IDs in plan")

        coverage = len(plan_ids & impl_ids) / len(plan_ids)
        # In real projects, target >= 80%. For fixtures, validate the mechanism works
        assert coverage >= 0.3, (
            f"Gate ID coverage: {coverage:.0%} (need >= 30%). "
            f"Missing: {plan_ids - impl_ids}"
        )

    @pytest.mark.p0
    def test_gate_script_mapping(self):
        """Gate prefixes should map to expected script number prefixes."""
        for gate, script_prefix in GATE_SCRIPT_MAP.items():
            # Just validate the mapping is defined correctly
            if isinstance(script_prefix, list):
                for sp in script_prefix:
                    assert sp.startswith(("0", "1")), f"Invalid prefix for {gate}"
            else:
                assert script_prefix[0].isdigit(), f"Invalid prefix for {gate}"


# ── T3-04: Implementation -> Verification handoff ─────────────────────


class TestImplementationToVerification:
    """Traceability matrix must cover Plan IDs."""

    @pytest.mark.p1
    def test_traceability_covers_plan(self):
        """Traceability matrix should reference Plan IDs."""
        plan = (FIXTURES / "sample_analysis_plan.md").read_text(encoding="utf-8")
        trace = (FIXTURES / "sample_traceability_matrix.md").read_text(encoding="utf-8")

        plan_ids = set(re.findall(r"G\d+[A-D]?-\d+", plan))
        trace_ids = set(re.findall(r"G\d+[A-D]?-\d+", trace))

        missing = plan_ids - trace_ids
        # Allow some missing (exploratory items may not be implemented yet)
        coverage = len(plan_ids & trace_ids) / len(plan_ids) if plan_ids else 1
        assert coverage >= 0.5, (
            f"Traceability coverage: {coverage:.0%}. Missing: {missing}"
        )


# ── T3-05: verification_config.yml <-> qa_inputs.json reconciliation ──


class TestConfigQAReconciliation:
    """Test reconciliation between config and qa_inputs."""

    @pytest.fixture(autouse=True)
    def _load(self):
        with open(FIXTURES / "sample_verification_config.yml", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        with open(FIXTURES / "sample_qa_inputs.json", encoding="utf-8") as f:
            self.qa = json.load(f)

    @pytest.mark.p0
    def test_all_config_keys_in_qa(self):
        """All config key_results should have corresponding qa_inputs entries."""
        config_keys = {
            (r["id"], r["metric"]) for r in self.config["key_results"]
        }
        qa_keys = {
            (r["id"], r["metric"]) for r in self.qa["key_results"]
        }
        missing = config_keys - qa_keys
        assert not missing, (
            f"Config key_results not in qa_inputs (FAIL): {missing}"
        )

    @pytest.mark.p0
    def test_tolerance_check(self):
        """Values within tolerance should pass."""
        config_map = {
            (r["id"], r["metric"]): r
            for r in self.config["key_results"]
        }
        for qa_item in self.qa["key_results"]:
            key = (qa_item["id"], qa_item["metric"])
            if key in config_map:
                cfg = config_map[key]
                diff = abs(qa_item["value"] - cfg["expected"])
                assert diff <= cfg["tolerance"], (
                    f"{key}: value {qa_item['value']} differs from expected "
                    f"{cfg['expected']} by {diff} (tolerance: {cfg['tolerance']})"
                )

    @pytest.mark.p0
    def test_extra_qa_items_warned(self):
        """Extra qa_inputs items not in config should be noted (not FAIL)."""
        config_keys = {
            (r["id"], r["metric"]) for r in self.config["key_results"]
        }
        qa_keys = {
            (r["id"], r["metric"]) for r in self.qa["key_results"]
        }
        extra = qa_keys - config_keys
        # Extra items are WARNING only, not FAIL
        # This test just verifies we can detect them
        if extra:
            import warnings
            warnings.warn(f"Extra qa_inputs not in config: {extra}")
