---
name: analysis-templates
description: Selects and reuses existing scripts and docs as templates for common analysis types (descriptive, survival, IPTW, time series).
---

# Template Selection

- Reuse existing scripts instead of starting from scratch; copy into `scripts/<analysis_name>/` and edit.
- Read prioritized docs before writing code:
  - `principles/compiled_principles.md`
  - `docs/r_usage_examples.md`
  - `docs/iptw_note.md`
  - `docs/troubleshooting.md`
  - `docs/summary.md`
  - `docs/r_environment_setup.md`
  - `docs/r_update_summary.md`
- Use repo-relative paths in commands; run from the repository root.
- Confirm with the user before adding new packages; use `scripts/verify_packages.R` to check availability.

## Script starting points

- General example: `scripts/updated_example.R`
- Basic demo: `scripts/simple_demo.R`
- Package checks: `scripts/verify_packages.R`

## Survival analysis

- Use `scripts/plos_analysis/fixed_cox_analysis.R`.
- Use `scripts/plos_analysis/cox_model_analysis.R`.
- Use `scripts/plos_analysis/data_exploration.R`.

## Time series

- Use `scripts/zenodo_analysis/spain_prediction_model.R`.
- Use `scripts/zenodo_analysis/zenodo_data_analysis.R`.

## New analysis workflow

- Create `scripts/<analysis_name>/`.
- Start with `00_readme.md` or `report.md`.
- Build scripts in order: `01_import_data.R`, `02_clean_data.R`, `03_descriptive_analysis.R`.
- Keep outputs inside the same folder and follow naming standards.

## Data wrangling scripts

- `01_import_data.R` - Data import and encoding handling.
- `02_clean_data.R` - Type conversion, missingness handling, outlier checks.
- For details, see the `data-wrangling` skill.
