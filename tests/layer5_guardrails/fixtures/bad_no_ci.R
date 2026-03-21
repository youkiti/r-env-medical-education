# Bad example: reports p-values without confidence intervals
# This violates analysis-guardrails non-negotiable rule #3

library(dplyr)

data <- read.csv("data/processed/analysis_data.csv")

model <- glm(outcome ~ treatment + age + sex, data = data, family = binomial)
summary_model <- summary(model)

# VIOLATION: Only reporting p-values, no confint() call
cat("Treatment effect p-value:", coef(summary_model)[2, "Pr(>|z|)"], "\n")
cat("Age p.value:", coef(summary_model)[3, "Pr(>|z|)"], "\n")

# Should also call: confint(model)
# Should also report: OR with 95% CI
