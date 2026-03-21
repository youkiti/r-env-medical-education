---
name: sap-authoring
description: Converts confirmed intake information into a Statistical Analysis Plan (SAP) and review checklist.
---

# SAP Authoring

## Scope

- Primary deliverable: `{project}/docs/statistical_analysis_plan.md`
- Secondary deliverable: `{project}/docs/code_review_checklist.md`
- This skill turns collected requirements into an approval-ready SAP.
- It does not assign Gate IDs, define script filenames, or create the project skeleton.

## Inputs

- Intake summary from `analysis-intake`
- Relevant constraints from `analysis-guardrails`, `data-privacy-handling`, and method skills

## Workflow position

```text
analysis-intake -> sap-authoring -> analysis-hitl-plan -> analysis-implementation -> code-review-companion
```

## Authoring workflow

1. Confirm that intake information is sufficiently complete for SAP drafting.
2. Convert confirmed facts into SAP sections without reopening settled decisions.
3. Highlight unresolved choices as explicit decision points.
4. Initialize a Decision log for future deviations.
5. Obtain review and approval before handoff to `analysis-hitl-plan`.

## SAP section structure

Use the following section headings as the canonical structure.

1. Document control
2. Background
3. Objectives and hypotheses
4. Study design and data source
5. Study population
6. Variables
7. Data processing plan
8. Statistical principles
9. Descriptive and exploratory analyses
10. Primary analysis
11. Secondary analyses
12. Subgroup analyses
13. Sensitivity analyses
14. Reproducibility and code operations
15. References
16. Decision log

## Authoring rules

- Distinguish confirmed facts from pending decisions.
- Keep exploratory analyses clearly labeled as exploratory.
- State assumptions, target estimands, and output expectations explicitly.
- Align reproducibility sections with `reproducibility-standards`.
- Align privacy and governance sections with `data-privacy-handling`.
- Align review sections with `code-review-companion`.

## Out of scope

- Gate numbering and `G<gate>-<seq>` assignment
- Canonical folder structure and numbered script layout
- Detailed package setup steps

## Handoff

- Pass the approved SAP to `analysis-hitl-plan` for Gate conversion.
- Pass any method-specific unresolved items to the relevant method skill before implementation.
