# Bad example: globally suppresses warnings
# This violates analysis-guardrails non-negotiable rule #5

options(warn = -1)

library(dplyr)

data <- read.csv("data/processed/analysis_data.csv")

model <- glm(outcome ~ treatment, data = data, family = binomial)
ci <- confint(model)
