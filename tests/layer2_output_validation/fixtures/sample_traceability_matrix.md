# Traceability Matrix

| Plan ID | Plan Description | Script | Line Range | Status |
|---------|-----------------|--------|------------|--------|
| G0A-1 | Verify R version | 00_setup.R | 5-10 | Implemented |
| G0B-1 | Import raw Excel data | 01_data_import.R | 12-25 | Implemented |
| G0B-2 | Validate variable types | 02_clean_data.R | 8-30 | Implemented |
| G0B-3 | Generate diagnostic matrix | 02_clean_data.R | 32-55 | Implemented |
| G1-1 | Generate Table 1 | 03_exploration.R | 10-45 | Implemented |
| G1-3 | Verify overall accuracy | 03_exploration.R | 47-60 | Implemented |
| G2A-1 | Diagnostic accuracy metrics | 04_descriptive_analysis.R | 15-40 | Implemented |
| G2B-1 | ROC curve generation | 05_primary_analysis.R | 10-30 | Implemented |
| G2B-2 | AUC with DeLong CI | 05_primary_analysis.R | 32-50 | Implemented |
| G2C-1 | Exclude <3 reviewers | 06_sensitivity_analysis.R | 8-25 | Partial |
| G2D-1 | Inter-rater reliability | 07_exploratory_analysis.R | 10-30 | Missing |
