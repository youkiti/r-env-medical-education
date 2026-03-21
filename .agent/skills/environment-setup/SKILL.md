---
name: environment-setup
description: Establishes the executable R environment for a project, including renv state, package availability, paths, and Windows-safe runtime conventions.
---

# Environment Setup

## Scope

- Primary deliverable: `setup_checklist.md`, `00_setup.R`, or an equivalent setup record.
- This skill owns environment readiness only.
- It does not define the analysis design, cleaning rules, or model specification.

## Required checks

- Confirm repository root and project root before running code.
- Record `R.version.string`, platform, and timezone assumptions.
- Confirm whether `renv` is active and whether `renv.lock` should be respected.
- List required packages and confirm availability before implementation starts.
- Confirm data source location and access method.

## Canonical package-availability pattern

- Prefer `scripts/verify_packages.R` for a first-pass inventory.
- Guard optional packages with `requireNamespace()` rather than unconditional `library()`.
- Ask the user before adding new packages.

```r
if (requireNamespace("readr", quietly = TRUE)) {
  df <- readr::read_csv(path)
} else {
  df <- read.csv(path, stringsAsFactors = FALSE)
}
```

## Path and execution conventions

- Resolve project paths from the repository root.
- Prefer `here::here()` plus `file.path()` for portable paths.
- Keep setup logic in `00_setup.R`; keep `_project_config.R` limited to path definitions with no side effects.

## Windows-safe runtime conventions

- PowerShell redirection may use CP932/Shift-JIS on Windows.
- Use English for `cat()` and `print()` messages in scripts that write to the console or redirected logs.
- Keep UTF-8-sensitive narrative output in Markdown or HTML files when possible.

## Handoff

- Pass environment readiness to `analysis-hitl-plan` Gate 0A and `analysis-implementation`.
- Refer to `reproducibility-standards` for naming and output conventions.
- Refer to `r-troubleshooting` when setup checks fail or package conflicts appear.
