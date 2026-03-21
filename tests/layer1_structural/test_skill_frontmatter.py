"""T1-01, T1-04: YAML frontmatter and naming convention tests."""

import re

import pytest

from tests.conftest import ACTIVE_SKILLS, SKILLS_DIR
from tests.helpers.yaml_validator import load_skill_frontmatter, validate_required_fields


# ── T1-01: YAML frontmatter existence and required fields ──────────────


class TestYAMLFrontmatter:
    """Validate all SKILL.md files have proper YAML frontmatter."""

    @pytest.fixture(autouse=True)
    def _setup(self, skill_files):
        self.skill_files = skill_files

    @pytest.mark.p0
    @pytest.mark.parametrize("skill_name", ACTIVE_SKILLS)
    def test_skill_md_exists(self, skill_name):
        """Each active skill must have a SKILL.md file."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        assert path.exists(), f"Missing SKILL.md for {skill_name}"

    @pytest.mark.p0
    @pytest.mark.parametrize("skill_name", ACTIVE_SKILLS)
    def test_has_frontmatter(self, skill_name):
        """Each SKILL.md must start with --- delimited YAML frontmatter."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n"), (
            f"{skill_name}/SKILL.md does not start with YAML frontmatter"
        )
        assert "\n---" in text[4:], (
            f"{skill_name}/SKILL.md has no closing --- for frontmatter"
        )

    @pytest.mark.p0
    @pytest.mark.parametrize("skill_name", ACTIVE_SKILLS)
    def test_required_fields(self, skill_name):
        """Frontmatter must contain 'name' and 'description' fields."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        fm = load_skill_frontmatter(path)
        assert fm is not None, f"Could not parse frontmatter for {skill_name}"
        missing = validate_required_fields(fm, ["name", "description"])
        assert not missing, (
            f"{skill_name} frontmatter missing fields: {missing}"
        )

    @pytest.mark.p0
    @pytest.mark.parametrize("skill_name", ACTIVE_SKILLS)
    def test_name_matches_directory(self, skill_name):
        """Frontmatter 'name' should match the directory name."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        fm = load_skill_frontmatter(path)
        assert fm is not None
        assert fm["name"] == skill_name, (
            f"Frontmatter name '{fm['name']}' != directory '{skill_name}'"
        )


# ── T1-04: Skill directory naming convention ──────────────────────────


class TestNamingConvention:
    """Validate skill directory naming follows kebab-case."""

    @pytest.mark.p1
    def test_all_kebab_case(self):
        """All skill directories must be kebab-case."""
        pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        dirs = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
        violations = [d for d in dirs if not pattern.match(d)]
        assert not violations, (
            f"Non-kebab-case skill directories: {violations}"
        )
