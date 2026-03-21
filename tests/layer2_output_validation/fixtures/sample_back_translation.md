# Back Translation Report

## G0B-1: Data Import

The script reads the raw Excel file containing 150 clinical case vignettes and loads it into a data frame.

## G0B-3: Diagnostic Accuracy Matrix

For each case, the script generates TP/FP/TN/FN classification based on whether ChatGPT's top diagnosis matches the reference standard.

## G1-3: Overall Accuracy Verification

The script computes the proportion of cases where ChatGPT's diagnosis was correct (answer_correct_bool == TRUE) and compares against the published value of 49.3%.

## G2B-1: ROC Curve

The script uses the pROC package to generate a ROC curve plotting sensitivity vs 1-specificity across all classification thresholds.

## G2B-2: AUC Computation

Area Under the ROC Curve is computed with DeLong confidence intervals using pROC::auc().
