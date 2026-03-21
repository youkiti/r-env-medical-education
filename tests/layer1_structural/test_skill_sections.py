"""T1-02, T1-03, T1-05: Skill section structure and AGENTS.md sync tests."""

import re

import pytest

from tests.conftest import ACTIVE_SKILLS, AGENTS_MD, SKILLS_DIR
from tests.helpers.markdown_parser import extract_headings


# ── T1-02: Required sections per skill ─────────────────────────────────

# Mapping of skill_name -> list of required H2 headings (substring match)
REQUIRED_SECTIONS = {
    "analysis-intake": ["Scope", "Study framing", "Outcome and exposure", "Variables and coding", "Reporting needs", "Handoff"],
    "sap-authoring": ["Scope", "Handoff"],
    "analysis-hitl-plan": ["Scope", "Handoff"],
    "environment-setup": ["Scope", "Handoff"],
    "data-wrangling": ["Scope", "Handoff"],
    "analysis-implementation": ["Scope", "Handoff"],
    "code-review-companion": ["Scope", "Stage A", "Stage B"],
    "analysis-guardrails": ["Scope", "Non-negotiable rules", "Enforcement logic"],
    "reproducibility-standards": ["Scope", "Handoff"],
    "data-privacy-handling": ["Scope", "Handoff"],
    "tdd-testthat": ["Scope"],
    "r-troubleshooting": ["Scope"],
    "causal-iptw-weightit": ["Scope", "Handoff"],
    "delegate-to-codex": ["Scope"],
}


class TestRequiredSections:
    """Validate each SKILL.md has its required sections."""

    @pytest.mark.p0
    @pytest.mark.parametrize("skill_name", ACTIVE_SKILLS)
    def test_has_scope_section(self, skill_name):
        """Every skill must have a ## Scope section."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        headings = extract_headings(text, level=2)
        scope_found = any("Scope" in h for h in headings)
        assert scope_found, f"{skill_name} missing ## Scope section"

    @pytest.mark.p0
    @pytest.mark.parametrize("skill_name", ACTIVE_SKILLS)
    def test_required_sections(self, skill_name):
        """Each skill must have its defined required sections."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        headings = extract_headings(text, level=2)

        required = REQUIRED_SECTIONS.get(skill_name, ["Scope"])
        missing = []
        for req in required:
            if not any(req in h for h in headings):
                missing.append(req)

        assert not missing, (
            f"{skill_name} missing required sections: {missing}. "
            f"Found headings: {headings}"
        )


# ── T1-03: AGENTS.md skill listing completeness ───────────────────────


class TestAgentsMdSync:
    """Validate AGENTS.md lists all active skills."""

    @pytest.mark.p0
    def test_all_skills_listed_in_agents_md(self):
        """Every skill directory should be referenced in AGENTS.md."""
        agents_text = AGENTS_MD.read_text(encoding="utf-8")
        actual_dirs = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}

        not_in_agents = []
        for skill in actual_dirs:
            # Check for the skill path pattern in AGENTS.md
            if skill not in agents_text:
                not_in_agents.append(skill)

        assert not not_in_agents, (
            f"Skills in .agent/skills/ but not mentioned in AGENTS.md: "
            f"{sorted(not_in_agents)}"
        )

    @pytest.mark.p0
    def test_agents_md_paths_exist(self):
        """Skill paths referenced in AGENTS.md should exist on disk."""
        agents_text = AGENTS_MD.read_text(encoding="utf-8")
        # Extract skill paths like .agent/skills/foo/SKILL.md
        paths = re.findall(
            r"\.agent/skills/([a-z0-9-]+)/SKILL\.md", agents_text
        )
        actual_dirs = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}

        missing = [p for p in paths if p not in actual_dirs]
        assert not missing, (
            f"AGENTS.md references non-existent skills: {missing}"
        )


# ── T1-05: Cross-skill reference validity ─────────────────────────────


class TestCrossReferences:
    """Validate skill-to-skill references point to existing skills."""

    @pytest.mark.p1
    @pytest.mark.parametrize("skill_name", ACTIVE_SKILLS)
    def test_referenced_skills_exist(self, skill_name):
        """Skill names referenced in backticks should be real skills."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        actual_dirs = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}

        # Find backtick-quoted references that look like skill names
        refs = re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`", text)

        # Filter to likely skill references (kebab-case with at least one hyphen)
        # Exclude common non-skill patterns
        non_skill = {
            "snake-case", "kebab-case", "back-translation",
            "cross-sectional", "quasi-experimental",
            "time-varying", "time-to-event", "per-protocol",
            "intent-to-treat", "semi-parametric",
        }

        invalid = []
        for ref in refs:
            if ref in non_skill:
                continue
            # Only check refs that match known skill naming patterns
            if ref in actual_dirs or ref in ACTIVE_SKILLS:
                continue
            # Check if it looks like a skill reference (exists in any skill list context)
            if any(
                f"`{ref}`" in line and ("skill" in line.lower() or "flag" in line.lower() or "→" in line or "pass" in line.lower() or "handoff" in line.lower())
                for line in text.split("\n")
            ):
                invalid.append(ref)

        assert not invalid, (
            f"{skill_name} references non-existent skills: {invalid}"
        )
