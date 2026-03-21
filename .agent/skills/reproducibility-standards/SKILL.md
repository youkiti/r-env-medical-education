---
name: reproducibility-standards
description: Defines naming, output, style, and session-recording conventions that make analysis projects readable and reproducible.
---

# Reproducibility Standards

## Scope

- Primary deliverable: a consistent project that can be read and rerun by another analyst.
- This skill owns general naming, output conventions, and reproducibility metadata.
- It does not own verification artifact names or test file naming.

## Script and file naming

- Data processing: `[NN]_<verb>_data.R`
- Analysis: `[NN]_<analysis>_analysis.R`
- Visualization: `[NN]_create_<target>.R`
- Report: `[NN]_generate_report.R`
- Utilities: `utils_<module>.R`
- Figure outputs: `<target>_<type>.png` and `<target>_<type>.pdf`

## Figure export

- Save figures in both PNG (300 dpi) and PDF formats.
- For standard ggplot objects, call `ggsave()` twice with identical size settings.
- For `survminer::ggsurvplot()` objects, print the returned object inside device functions.

```r
p <- ggsurvplot(fit, data = df, ...)

png("output.png", width = 10, height = 8, units = "in", res = 300)
print(p)
dev.off()

pdf("output.pdf", width = 10, height = 8)
print(p)
dev.off()
```

## Session recording

- Record execution date, R version, platform, and loaded package versions in the analysis folder.
- Save session metadata near the analysis outputs, for example `output/session_info.txt`.

## Code style

- Follow tidyverse-style snake_case naming.
- Use one pipe style consistently (`|>` or `%>%`).
- Write short Japanese comments only where the logic is not obvious.
- Set `set.seed(123)` when randomness is used.

## Cleanup

- Remove scratch files such as `_v2` and `_simple` before finishing.
- Leave scripts in a clear execution order.

## Handoff

- `code-review-companion` owns verification artifact filenames and traceability rules.
- `tdd-testthat` owns `test-<module>.R` and test helper naming.
- `environment-setup` owns Windows-specific runtime cautions and package-availability checks.
