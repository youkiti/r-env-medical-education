"""T2-04: Analysis plan Gate ID structural validation."""

import pathlib
import re
from collections import Counter

import pytest

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


class TestAnalysisPlan:
    """Validate analysis_plan.md Gate structure."""

    @pytest.fixture(autouse=True)
    def _load(self):
        self.text = (FIXTURES / "sample_analysis_plan.md").read_text(encoding="utf-8")
        self.gate_ids = re.findall(r"G\d+[A-D]?-\d+", self.text)

    @pytest.mark.p0
    def test_has_required_gates(self):
        """Plan must contain Gate 0A, 0B, 1, 2A, 2B at minimum."""
        required = ["Gate 0A", "Gate 0B", "Gate 1", "Gate 2A", "Gate 2B"]
        missing = [g for g in required if g not in self.text]
        assert not missing, f"Missing required gates: {missing}"

    @pytest.mark.p0
    def test_has_gate_ids(self):
        """Plan must contain at least 5 G<gate>-<seq> IDs."""
        assert len(self.gate_ids) >= 5, (
            f"Expected >= 5 Gate IDs, found {len(self.gate_ids)}: {self.gate_ids}"
        )

    @pytest.mark.p0
    def test_no_duplicate_ids(self):
        """All Gate IDs must be unique."""
        counts = Counter(self.gate_ids)
        dupes = {k: v for k, v in counts.items() if v > 1}
        assert not dupes, f"Duplicate Gate IDs: {dupes}"

    @pytest.mark.p0
    def test_id_format_valid(self):
        """All IDs must match G<gate>-<seq> pattern."""
        pattern = re.compile(r"^G\d+[A-D]?-\d+$")
        invalid = [gid for gid in self.gate_ids if not pattern.match(gid)]
        assert not invalid, f"Invalid Gate ID format: {invalid}"

    @pytest.mark.p0
    def test_sequential_within_gates(self):
        """Sequence numbers within each gate should be consecutive."""
        # Group by gate prefix
        from collections import defaultdict
        gate_groups = defaultdict(list)
        for gid in self.gate_ids:
            match = re.match(r"(G\d+[A-D]?)-(\d+)", gid)
            if match:
                gate_groups[match.group(1)].append(int(match.group(2)))

        for gate, seqs in gate_groups.items():
            seqs.sort()
            expected = list(range(seqs[0], seqs[0] + len(seqs)))
            assert seqs == expected, (
                f"Gate {gate} has non-consecutive sequences: {seqs}"
            )
