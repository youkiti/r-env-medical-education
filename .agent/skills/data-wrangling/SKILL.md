---
name: data-wrangling
description: Implements Gate 0B data import, type checks, missingness diagnosis, and cleaning rules.
---

# Data Wrangling (Gate 0B Implementation)

## Scope

- Primary deliverable: a cleaned analysis-ready dataset plus a cleaning log.
- This skill implements approved cleaning rules.
- It does not define privacy policy, project structure, or modeling strategy.

## 1. Data import

- Confirm file types such as CSV, Excel, and RDS.
- Handle encoding issues, including UTF-8 and CP932/Shift-JIS.
- Use package guards defined in `environment-setup`.

## 2. Type verification and conversion

- Review types with `str()` and `summary()`.
- Convert character, factor, date, and numeric fields as required by the plan.
- Record conversions that affect interpretation or units.
- Verify event/status variables with `table()` (for example `table(df$status)`) and reconcile the observed categories against the paper's reported counts before modeling. Never infer event coding from column names; skipping this step can produce entirely wrong survival/outcome results and waste debugging time.

## 3. Sentinel value handling

> [!CAUTION]
> Converting sentinel values is a statistical decision.
> Confirm with the codebook and the user before applying changes.

- Document confirmed sentinel rules in the cleaning log.
- Apply conversions only after confirmation.

## 4. Missing data diagnosis

- Quantify missingness with `colMeans(is.na(df))` or equivalent.
- Summarize missingness for key analysis variables.
- Use optional visualizations when useful, but keep the missing-data rule itself aligned with the approved plan.

## 5. Data cleaning

- Check logical ranges and impossible values.
- Review duplicates and repeated rows.
- Document outlier rules and whether they affect the main dataset or only sensitivity analyses.

## 6. Variable mapping documentation

- Map source column names to paper or SAP terms.
- Record units and any required unit conversions.
- Keep the mapping accessible to downstream scripts and reviewers.

## 7. Outputs and logging

- Save the cleaning log with row counts, exclusions, sentinel handling, and type changes.
- Store cleaned data only in locations allowed by `data-privacy-handling`.
- Follow `reproducibility-standards` for script names and output naming.

## Handoff

- Pass cleaned data and the cleaning log to Gate 1 and Gate 2 analyses.
- If cleaning rules change the approved plan, return to `analysis-hitl-plan` Gate 0B.
