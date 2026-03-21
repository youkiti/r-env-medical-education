---
name: data-privacy-handling
description: Handles sensitive data placement, git hygiene, and synthetic-data-first verification.
---

# Data Privacy and Handling

## Scope

- This skill owns privacy-safe storage and output rules.
- It does not define cleaning logic or statistical modeling.

## Rules

- Do not commit sensitive or personal data.
- Store private datasets under `data/private/` or an equivalent gitignored private location.
- Keep `.gitignore` aligned with all private-data paths and temporary exports.
- Validate code on synthetic or sample data before running on real data.
- Avoid including raw private data in outputs, logs, snapshots, or verification artifacts.
- Treat intermediate cleaned data and QA exports as sensitive unless explicitly cleared for sharing.

## Handoff

- `data-wrangling` follows these storage rules.
- `tdd-testthat` uses synthetic fixtures instead of real patient-level data.
- `code-review-companion` must avoid embedding raw data into verification outputs.
