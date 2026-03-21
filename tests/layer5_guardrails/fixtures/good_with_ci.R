# Good example: properly reports estimates with confidence intervals

library(dplyr)

data <- read.csv("data/processed/analysis_data.csv")

model <- glm(outcome ~ treatment + age + sex, data = data, family = binomial)

# Compute confidence intervals
ci <- confint(model)
or_est <- exp(coef(model))
or_ci <- exp(ci)

cat("Treatment OR:", round(or_est[2], 2),
    "(95% CI:", round(or_ci[2, 1], 2), "-", round(or_ci[2, 2], 2), ")\n")
cat("p-value:", round(coef(summary(model))[2, 4], 4), "\n")
