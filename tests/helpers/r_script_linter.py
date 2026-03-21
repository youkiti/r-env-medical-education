"""R script convention checking utilities."""

from __future__ import annotations

import re
import pathlib


def strip_r_comments(content: str) -> str:
    """Remove comment lines and inline comments from R code.

    Preserves string literals by only stripping # outside quotes.
    """
    lines = []
    for line in content.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        in_string = False
        quote_char = None
        result = []
        for i, ch in enumerate(line):
            if ch in ('"', "'") and (i == 0 or line[i - 1] != "\\"):
                if not in_string:
                    in_string = True
                    quote_char = ch
                elif ch == quote_char:
                    in_string = False
            if ch == "#" and not in_string:
                break
            result.append(ch)
        lines.append("".join(result))
    return "\n".join(lines)


def check_naming_convention(filename: str) -> bool:
    """Check if R script filename follows naming conventions.

    Valid patterns:
    - Numbered scripts: NN_<verb>_<noun>.R  (e.g., 01_import_data.R)
    - Utils: utils_<module>.R
    - Tests: test-<module>.R
    - Special: _project_config.R, run_all.R, testthat.R
    """
    special = {"_project_config.R", "run_all.R", "testthat.R"}
    if filename in special:
        return True
    patterns = [
        r"^\d{2}_[a-z][a-z0-9_]*\.R$",  # numbered scripts
        r"^utils_[a-z][a-z0-9_]*\.R$",  # utilities
        r"^test-[a-z][a-z0-9_]*\.R$",  # test files
        r"^helper-[a-z][a-z0-9_]*\.R$",  # test helpers
    ]
    return any(re.match(p, filename) for p in patterns)


def extract_plan_ids(content: str) -> list[str]:
    """Extract @plan_id tags from R script content."""
    return re.findall(r"@plan_id\s+(G\d+[A-D]?-\d+)", content)


def detect_side_effects(content: str) -> list[str]:
    """Detect side-effect patterns that should not appear in utils_*.R (code only)."""
    code = strip_r_comments(content)
    violations = []
    patterns = {
        "library()": r"\blibrary\(",
        "require()": r"\brequire\(",
        "source()": r"\bsource\(",
        "<<- assignment": r"<<-",
        "options()": r"\boptions\(",
    }
    for name, pattern in patterns.items():
        if re.search(pattern, code):
            violations.append(name)
    return violations


def detect_ci_patterns(content: str) -> bool:
    """Check if content contains CI computation patterns (code only, comments stripped)."""
    code = strip_r_comments(content)
    ci_patterns = [
        r"\bconfint\(",
        r"\bconf\.int\b",
        r"conf\.level",
        r"confidence[._]interval",
    ]
    return any(re.search(p, code, re.IGNORECASE) for p in ci_patterns)


def detect_pvalue_patterns(content: str) -> bool:
    """Check if content contains p-value reporting patterns (code only)."""
    code = strip_r_comments(content)
    pvalue_patterns = [
        r"\bp[._\-]value\b",
        r"\bpvalue\b",
        r"\bp\.val\b",
        r"Pr\(>",
    ]
    return any(re.search(p, code, re.IGNORECASE) for p in pvalue_patterns)


def detect_stat_functions(content: str) -> bool:
    """Check if content contains statistical function calls (code only)."""
    code = strip_r_comments(content)
    stat_funcs = [
        r"\blm\(", r"\bglm\(", r"\bt\.test\(", r"\bchisq\.test\(",
        r"\bwilcox\.test\(", r"\bfisher\.test\(", r"\bprop\.test\(",
        r"\bcox(ph)?\(", r"\bsurvfit\(", r"\blogrank\(",
        r"\bcor\.test\(", r"\banova\(", r"\bkruskal\.test\(",
    ]
    return any(re.search(p, code) for p in stat_funcs)


def detect_random_functions(content: str) -> bool:
    """Check if content uses random number generation (code only)."""
    code = strip_r_comments(content)
    rng_patterns = [
        r"\bsample\(", r"\brnorm\(", r"\brunif\(",
        r"\brbinom\(", r"\brpois\(", r"\bboot\(",
        r"\bsample_n\(", r"\bsample_frac\(",
    ]
    return any(re.search(p, code) for p in rng_patterns)


def detect_set_seed(content: str) -> bool:
    """Check if set.seed() is called (code only)."""
    code = strip_r_comments(content)
    return bool(re.search(r"\bset\.seed\(", code))


def detect_global_warning_suppression(content: str) -> bool:
    """Check for global warning suppression (not local suppressWarnings())."""
    code = strip_r_comments(content)
    return bool(re.search(r"options\(\s*warn\s*=\s*-1\s*\)", code))


def find_r_scripts(project_dir: pathlib.Path) -> list[pathlib.Path]:
    """Find all .R files in a project's scripts/ directory."""
    scripts_dir = project_dir / "scripts"
    if not scripts_dir.exists():
        return []
    return sorted(scripts_dir.glob("*.R"))
