"""YAML frontmatter validation utilities."""

from __future__ import annotations

import pathlib

import yaml

from .markdown_parser import extract_frontmatter


def load_skill_frontmatter(skill_path: pathlib.Path) -> dict | None:
    """Load and parse YAML frontmatter from a SKILL.md file."""
    text = skill_path.read_text(encoding="utf-8")
    return extract_frontmatter(text)


def validate_required_fields(
    frontmatter: dict, required: list[str]
) -> list[str]:
    """Return list of missing required fields."""
    return [f for f in required if not frontmatter.get(f)]


def load_yaml_file(path: pathlib.Path) -> dict:
    """Load a YAML file and return parsed dict."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)
