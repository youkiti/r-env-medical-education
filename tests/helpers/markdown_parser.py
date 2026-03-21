"""Markdown section extraction utilities."""

from __future__ import annotations

import re


def extract_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from markdown text.

    Returns parsed dict or None if no frontmatter found.
    """
    import yaml

    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def extract_headings(text: str, level: int = 2) -> list[str]:
    """Extract all headings of given level from markdown text."""
    pattern = rf"^{'#' * level}\s+(.+)$"
    return re.findall(pattern, text, re.MULTILINE)


def extract_sections(text: str, level: int = 2) -> dict[str, str]:
    """Extract heading -> content mapping for given level."""
    pattern = rf"^({'#' * level}\s+.+)$"
    parts = re.split(pattern, text, flags=re.MULTILINE)
    sections = {}
    for i in range(1, len(parts), 2):
        heading = parts[i].lstrip("#").strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections[heading] = content.strip()
    return sections


def extract_table_headers(text: str) -> list[list[str]]:
    """Extract header rows from all markdown tables in text."""
    tables = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|", lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            tables.append(headers)
    return tables


def extract_checkboxes(text: str) -> list[str]:
    """Extract checkbox items (- [ ] or - [x]) from markdown."""
    return re.findall(r"^- \[[ x]\]\s+(.+)$", text, re.MULTILINE)
