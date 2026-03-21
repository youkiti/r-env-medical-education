---
name: analysis-hitl-plan
description: Converts an approved SAP into a Gate-based implementation plan with numbered decisions, approval points, and `G<gate>-<seq>` IDs.
---

# Human-in-the-Loop Plan

## Scope

- Primary deliverable: `{project}/analysis_plan.md`
- This skill converts an approved SAP into an implementation contract.
- It does not own model-specific diagnostic details or environment setup procedures.

## Gate sequence

```text
Phase 0: Data Preparation
  |- Gate 0A: Environment Setup
  `- Gate 0B: Data Cleaning Plan
Phase 1: Data Exploration
  `- Gate 1: Exploration
Phase 2: Data Analyses
  |- Gate 2A: Descriptive Statistics Plan
  |- Gate 2B: Main Analysis Plan
  |- Gate 2C: Sensitivity Analysis Plan
  `- Gate 2D: Exploratory Analysis Plan
```

## Planning rules

- Assign every planned implementation item an ID in the form `G<gate>-<seq>`.
- Record approval status, owner, inputs, outputs, and fallback action for each Gate item.
- Convert SAP text into executable plan items; do not restate the full SAP.

## Gate content

### Gate 0A: Environment Setup

- Record required R version, key packages, path assumptions, and setup blockers.
- Refer to `environment-setup` for implementation detail.

### Gate 0B: Data Cleaning Plan

- Record variable mapping, inclusion and exclusion rules, missing-data handling rules, and expected sample counts.
- If custom functions are needed, record the need for tests and hand off implementation to `tdd-testthat`.

### Gate 1: Exploration

- Record required exploratory plots and summaries.
- Document what findings must be brought forward into Gate 2B discussion.

### Gate 2A: Descriptive Statistics Plan

- Record Table 1 structure, stratification, summary statistics, and output destinations.

### Gate 2B: Main Analysis Plan

- Record formula, covariates, reference categories, estimand, and output specification.
- For each assumption check, record:
  - `check`
  - `source_skill`
  - `required` or `recommended`
  - `trigger`
  - `fail_action`
- Keep the agreement table here, but keep detailed check procedures in the relevant method skill.

### Gate 2C: Sensitivity Analysis Plan

- Record alternative definitions, alternative model specifications, trimming rules, and planned comparisons with the main analysis.

### Gate 2D: Exploratory Analysis Plan

- Record subgroup analyses, interaction terms, and the labeling of exploratory outputs.

## Required routing rules

- Required check fails -> return to Gate 2B and re-approve.
- Recommended check triggers -> route to Gate 2C unless the issue changes the main model specification.
- Environment blockers -> return to Gate 0A.
- Data-definition blockers -> return to Gate 0B.

## Handoff

- `analysis-implementation` uses this plan as the source for file layout and `@plan_id` placement.
- `code-review-companion` uses the IDs as the source of traceability.
- Method skills such as `causal-iptw-weightit` own the detailed diagnostic checklists.
