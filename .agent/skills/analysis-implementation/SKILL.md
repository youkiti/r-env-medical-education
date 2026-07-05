---
name: analysis-implementation
description: Converts an approved Gate-based analysis plan into a project skeleton, numbered scripts, and reusable implementation templates under projects/.
---

# Analysis Implementation

## Scope

- Primary deliverable: `projects/<analysis_name>/` with executable script skeletons.
- This skill owns the translation from approved plan to code structure.
- This skill also owns the single-file Rmd education-mode structure (see "Lightweight Rmd mode").
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
- Candidate sources (real, in-repo):
  - `projects/medical_education_admissions/` — multiple regression example.
  - `projects/medical_education_panel/` — ITS/DID example.
  - `projects/chatgpt_diagnostic_study/` — diagnostic-accuracy example.
  - `scripts/zenodo_analysis/` — script-level example.
  - `scripts/archive/` — older sample scripts; reference only as a last resort.
- Copy the closest template into the project skeleton and adapt it to approved Gate IDs.

## Implementation rules

- Keep numbered scripts aligned with Gate order.
- Put `@plan_id` tags in numbered scripts, not in `utils_*.R`.
- Keep helper functions in `utils_*.R` and test them through `tdd-testthat`.
- Keep outputs inside the project folder and follow `reproducibility-standards`.

## Lightweight Rmd mode (education)

- When to use: education handsons and small analyses may use a single-Rmd mode. Real research projects use the numbered-script structure above. The numbered structure is the default; use Rmd mode only when the user specifies an Rmd.
- Structure: one `projects/<analysis_name>/analysis.Rmd` plus `output/` and `data/`. Order the Rmd section headings to match Gate order: Setup -> Import -> Clean -> Explore -> Descriptive -> Primary -> Sensitivity.
- Traceability: put `@plan_id` tags as in-chunk comments (same format as the numbered-script rule). Reflect the Gate ID in the chunk label as well, for example ` ```{r g2b-1-primary-model} `.
- Guardrails are unchanged: `analysis-guardrails` and `data-privacy-handling` apply fully in Rmd mode.

## Handoff

- `code-review-companion` owns verification artifacts and verification file naming.
- `reproducibility-standards` owns general naming, figure export, and session documentation.
- `data-privacy-handling` owns where sensitive data may be stored.
