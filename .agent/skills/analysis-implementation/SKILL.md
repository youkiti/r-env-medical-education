---
name: analysis-implementation
description: Converts an approved Gate-based analysis plan into a project skeleton, numbered scripts, and reusable implementation templates under projects/.
---

# Analysis Implementation

## Scope

- Primary deliverable: `projects/<analysis_name>/` with executable script skeletons.
- This skill owns the translation from approved plan to code structure.
- It does not replace SAP approval, Gate approval, or statistical judgment.

## Inputs

- Approved `analysis_plan.md`
- Environment readiness from `environment-setup`
- Relevant method skills such as `causal-iptw-weightit`

## Canonical project structure

```text
projects/<analysis_name>/
|-- README.md
|-- analysis_plan.md
|-- verification_config.yml
|-- docs/
|   |-- statistical_analysis_plan.md
|   `-- data_dictionary.csv
|-- scripts/
|   |-- _project_config.R
|   |-- 00_setup.R
|   |-- 01_data_import.R
|   |-- 02_clean_data.R
|   |-- 03_exploration.R
|   |-- 04_descriptive_analysis.R
|   |-- 05_primary_analysis.R
|   |-- 06_sensitivity_analysis.R
|   |-- 07_exploratory_analysis.R
|   |-- run_all.R
|   `-- 99_verify_data.R
|-- tests/
|   `-- testthat/
`-- output/
    |-- figures/
    |-- tables/
    `-- verification/
```

## Gate-to-script mapping

- Gate 0A -> `00_setup.R`
- Gate 0B -> `01_data_import.R`, `02_clean_data.R`
- Gate 1 -> `03_exploration.R`
- Gate 2A -> `04_descriptive_analysis.R`
- Gate 2B -> `05_primary_analysis.R`
- Gate 2C -> `06_sensitivity_analysis.R`
- Gate 2D -> `07_exploratory_analysis.R`
- Verification -> `run_all.R`, `99_verify_data.R`

## Reuse-first workflow

- Reuse existing examples before starting from scratch.
- Candidate sources:
  - `scripts/updated_example.R`
  - `scripts/simple_demo.R`
  - `scripts/plos_analysis/`
  - `scripts/zenodo_analysis/`
- Copy the closest template into the project skeleton and adapt it to approved Gate IDs.

## Implementation rules

- Keep numbered scripts aligned with Gate order.
- Put `@plan_id` tags in numbered scripts, not in `utils_*.R`.
- Keep helper functions in `utils_*.R` and test them through `tdd-testthat`.
- Keep outputs inside the project folder and follow `reproducibility-standards`.

## Handoff

- `code-review-companion` owns verification artifacts and verification file naming.
- `reproducibility-standards` owns general naming, figure export, and session documentation.
- `data-privacy-handling` owns where sensitive data may be stored.
