# Bad example: hardcodes statistical results without computation
# This violates analysis-guardrails non-negotiable rule #1

library(dplyr)

data <- read.csv("data/processed/analysis_data.csv")

# VIOLATION: No statistical function call, results are fabricated
cat("Primary analysis results:\n")
cat("Odds Ratio: 2.45 (95% CI: 1.23-4.87)\n")
cat("p-value: 0.011\n")
cat("The treatment showed a statistically significant effect.\n")

# No lm(), glm(), t.test(), or any statistical computation
