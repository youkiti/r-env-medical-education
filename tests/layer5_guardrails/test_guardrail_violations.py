"""T5-01, T5-02, T5-05, T5-06, T5-07, T5-08, T5-09: Guardrail violation tests."""

import json
import pathlib
import re

import pytest

from tests.helpers.r_script_linter import (
    detect_ci_patterns,
    detect_global_warning_suppression,
    detect_pvalue_patterns,
    detect_random_functions,
    detect_set_seed,
    detect_stat_functions,
)

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


# ── T5-01: Detect statistical report without confidence interval ───────


class TestNoCIDetection:
    """Detect p-value reporting without CI."""

    @pytest.mark.p0
    def test_bad_no_ci_detected(self):
        """Script with p-values but no CI should be flagged."""
        content = (FIXTURES / "bad_no_ci.R").read_text(encoding="utf-8")
        has_pvalue = detect_pvalue_patterns(content)
        has_ci = detect_ci_patterns(content)
        assert has_pvalue, "Should detect p-value patterns"
        assert not has_ci, "Should NOT detect CI patterns in bad file"

    @pytest.mark.p0
    def test_good_with_ci_not_flagged(self):
        """Script with both p-values and CI should not be flagged."""
        content = (FIXTURES / "good_with_ci.R").read_text(encoding="utf-8")
        has_pvalue = detect_pvalue_patterns(content)
        has_ci = detect_ci_patterns(content)
        assert has_pvalue, "Should detect p-value patterns"
        assert has_ci, "Should detect CI patterns in good file"


# ── T5-02: Detect fabricated/hardcoded results ─────────────────────────


class TestFabricatedResults:
    """Detect hardcoded results without statistical computation."""

    @pytest.mark.p0
    def test_bad_fabricated_detected(self):
        """Script with no stat functions but result output should be flagged."""
        content = (FIXTURES / "bad_fabricated_results.R").read_text(encoding="utf-8")
        has_stat = detect_stat_functions(content)
        assert not has_stat, "Should NOT detect stat functions in fabricated file"

    @pytest.mark.p0
    def test_good_has_stat_functions(self):
        """Script with stat functions should not be flagged."""
        content = (FIXTURES / "good_with_ci.R").read_text(encoding="utf-8")
        has_stat = detect_stat_functions(content)
        assert has_stat, "Should detect stat functions in good file"


# ── T5-06: Detect global warning suppression ───────────────────────────


class TestGlobalWarningSuppression:
    """Detect options(warn = -1) global suppression."""

    @pytest.mark.p1
    def test_bad_global_suppress_detected(self):
        """Script with options(warn = -1) should be flagged."""
        content = (FIXTURES / "bad_global_suppress.R").read_text(encoding="utf-8")
        assert detect_global_warning_suppression(content)

    @pytest.mark.p1
    def test_good_no_global_suppress(self):
        """Normal script should not be flagged."""
        content = (FIXTURES / "good_with_ci.R").read_text(encoding="utf-8")
        assert not detect_global_warning_suppression(content)


# ── T5-07: Detect missing set.seed() ──────────────────────────────────


class TestMissingSetSeed:
    """Detect random functions without prior set.seed()."""

    @pytest.mark.p2
    def test_bad_no_seed_detected(self):
        """Script with random functions but no set.seed should be flagged."""
        content = (FIXTURES / "bad_no_seed.R").read_text(encoding="utf-8")
        has_random = detect_random_functions(content)
        has_seed = detect_set_seed(content)
        assert has_random, "Should detect random functions"
        assert not has_seed, "Should NOT detect set.seed in bad file"

    @pytest.mark.p2
    def test_good_with_seed_not_flagged(self):
        """Script with set.seed before random functions is fine."""
        content = "set.seed(123)\nx <- sample(100, 50)\n"
        has_random = detect_random_functions(content)
        has_seed = detect_set_seed(content)
        assert has_random
        assert has_seed


# ── T5-05: Detect causal claims without limitations ───────────────────


class TestCausalClaims:
    """Detect causal language without limitation/assumption context."""

    CAUSAL_PATTERNS = [
        r"\bcaused?\b",
        r"\bcausal\s+effect\b",
        r"\beffectively\s+prevents?\b",
    ]
    LIMITATION_PATTERNS = [
        r"\blimitation",
        r"\bassumption",
        r"\bobservational",
        r"\bconfound",
    ]

    def _has_causal(self, text: str) -> bool:
        return any(re.search(p, text, re.IGNORECASE) for p in self.CAUSAL_PATTERNS)

    def _has_limitations(self, text: str) -> bool:
        return any(re.search(p, text, re.IGNORECASE) for p in self.LIMITATION_PATTERNS)

    @pytest.mark.p1
    def test_bad_causal_without_limitations(self):
        """Causal claims without limitation context should be flagged."""
        text = (FIXTURES / "bad_causal_claims.md").read_text(encoding="utf-8")
        has_causal = self._has_causal(text)
        has_limits = self._has_limitations(text)
        assert has_causal, "Should detect causal language"
        assert not has_limits, "Should NOT find limitation language in bad file"

    @pytest.mark.p1
    def test_good_causal_with_limitations(self):
        """Causal claims with limitations context should pass."""
        text = (FIXTURES / "good_causal_claims.md").read_text(encoding="utf-8")
        has_causal = self._has_causal(text)
        has_limits = self._has_limitations(text)
        assert has_causal, "Should detect causal language"
        assert has_limits, "Should find limitation language in good file"


# ── T5-08: Invalid status values in qa_inputs.json ────────────────────


class TestInvalidQAStatus:
    """Detect invalid status values in qa_inputs.json."""

    @pytest.mark.p1
    def test_bad_status_detected(self):
        """qa_inputs with invalid status 'unknown' should be flagged."""
        with open(FIXTURES / "bad_qa_inputs.json", encoding="utf-8") as f:
            qa = json.load(f)
        valid = {"pass", "fail", "skipped"}
        invalid = [
            c for c in qa.get("assumption_checks", [])
            if c.get("status") not in valid
        ]
        assert len(invalid) > 0, "Should detect invalid status value"

    @pytest.mark.p1
    def test_good_status_passes(self):
        """qa_inputs with valid statuses should pass."""
        fixtures_l2 = FIXTURES.parent.parent / "layer2_output_validation" / "fixtures"
        with open(fixtures_l2 / "sample_qa_inputs.json", encoding="utf-8") as f:
            qa = json.load(f)
        valid = {"pass", "fail", "skipped"}
        invalid = [
            c for c in qa.get("assumption_checks", [])
            if c.get("status") not in valid
        ]
        assert len(invalid) == 0, f"Unexpected invalid statuses: {invalid}"


# ── T5-09: required + skipped = FAIL ──────────────────────────────────


class TestRequiredSkippedFail:
    """Required assumption checks that are skipped must be FAIL."""

    @pytest.mark.p0
    def test_required_skipped_is_fail(self):
        """required=true + status=skipped should trigger FAIL."""
        with open(FIXTURES / "bad_required_skipped.json", encoding="utf-8") as f:
            qa = json.load(f)

        failures = []
        for check in qa.get("assumption_checks", []):
            if check.get("required") and check.get("status") == "skipped":
                failures.append(check["id"])

        assert len(failures) > 0, (
            "Should detect required+skipped as FAIL condition"
        )

    @pytest.mark.p0
    def test_recommended_skipped_is_ok(self):
        """required=false + status=skipped should NOT trigger FAIL."""
        qa = {
            "assumption_checks": [
                {
                    "id": "G2D-1",
                    "model": "exploratory",
                    "check": "optional_check",
                    "required": False,
                    "result": "",
                    "status": "skipped",
                }
            ]
        }
        failures = [
            c["id"]
            for c in qa["assumption_checks"]
            if c.get("required") and c.get("status") == "skipped"
        ]
        assert len(failures) == 0, "recommended+skipped should not be FAIL"
