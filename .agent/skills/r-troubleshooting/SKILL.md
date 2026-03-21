---
name: r-troubleshooting
description: Triages R errors with reproducible steps, environment checks, and function disambiguation.
---

# R Troubleshooting

## Scope

- Primary deliverable: a reproducible issue report with likely cause and next check.
- This skill handles runtime and package-level problems after setup has started.
- Baseline environment readiness belongs to `environment-setup`.

## Workflow

1. Capture the exact command and full error message.
2. Capture `sessionInfo()`, package versions, and relevant object structure with `str()` or `names()`.
3. Check path assumptions, object classes, and missing packages.
4. Disambiguate namespace conflicts with `pkg::fun()`.
5. Consult `docs/troubleshooting.md` for known issues and fixes.

## Escalation

- If the issue is missing packages or path assumptions, return to `environment-setup`.
- If the issue comes from project-specific helper functions, add or run tests with `tdd-testthat`.
- If the issue changes the agreed analysis behavior, return to `analysis-hitl-plan`.
