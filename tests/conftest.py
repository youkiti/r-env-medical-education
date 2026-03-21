"""Shared fixtures and path definitions for skill tests."""

import pathlib

import pytest

# Repository root
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agent" / "skills"
ARCHIVED_SKILLS_DIR = REPO_ROOT / ".agent" / "archived-skills"
PROJECTS_DIR = REPO_ROOT / "projects"
AGENTS_MD = REPO_ROOT / "AGENTS.md"

# Active skill names (expected)
ACTIVE_SKILLS = [
    "analysis-intake",
    "sap-authoring",
    "analysis-hitl-plan",
    "environment-setup",
    "data-wrangling",
    "analysis-implementation",
    "code-review-companion",
    "analysis-guardrails",
    "reproducibility-standards",
    "data-privacy-handling",
    "tdd-testthat",
    "r-troubleshooting",
    "causal-iptw-weightit",
    "delegate-to-codex",
]


def pytest_configure(config):
    config.addinivalue_line("markers", "p0: P0 priority (must-have)")
    config.addinivalue_line("markers", "p1: P1 priority (should-have)")
    config.addinivalue_line("markers", "p2: P2 priority (nice-to-have)")
    config.addinivalue_line("markers", "requires_r: requires R runtime")


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture
def skills_dir():
    return SKILLS_DIR


@pytest.fixture
def projects_dir():
    return PROJECTS_DIR


@pytest.fixture
def skill_files():
    """Return dict of {skill_name: Path to SKILL.md}."""
    return {
        d.name: d / "SKILL.md"
        for d in sorted(SKILLS_DIR.iterdir())
        if d.is_dir() and (d / "SKILL.md").exists()
    }
