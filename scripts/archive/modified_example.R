# Modified example R script for clinical epidemiology analysis
# Using available packages: ggplot2, dplyr, WeightIt
# Note: tidyverse and gtsummary could not be installed due to version constraints

# Load required libraries
library(ggplot2)    # Advanced plotting
library(dplyr)      # Data manipulation
library(WeightIt)   # Inverse probability weighting
library(tidyr)      # Data reshaping (tidyverse component)
library(readr)      # Data import (tidyverse component)
library(purrr)      # Functional programming (tidyverse component)
library(tibble)     # Modern data frames (tidyverse component)
library(stringr)    # String manipulation (tidyverse component)
library(forcats)    # Factor manipulation (tidyverse component)

# Print loaded package versions
cat("Loaded packages:\n")
cat("---------------\n")
pkgs <- c("ggplot2", "dplyr", "WeightIt", "tidyr", "readr", "purrr", "tibble", "stringr", "forcats")
for(pkg in pkgs) {
  if(pkg %in% rownames(installed.packages())) {
    ver <- packageVersion(pkg)
    cat(sprintf("✓ %s version %s\n", pkg, ver))
  } else {
    cat(sprintf("✗ %s not installed\n", pkg))
  }
}
cat("\n")

# Example 1: Data preparation and descriptive statistics
# --------------------------------------------------

# Create example dataset
set.seed(123)
n <- 500
example_data <- tibble(
  id = 1:n,
  age = rnorm(n, mean = 50, sd = 15),
  sex = factor(sample(c("Male", "Female"), n, replace = TRUE, prob = c(0.45, 0.55))),
  treatment = factor(sample(c("Treatment A", "Treatment B"), n, replace = TRUE)),
  bmi = rnorm(n, mean = 25, sd = 5),
  smoker = factor(sample(c("Yes", "No"), n, replace = TRUE, prob = c(0.3, 0.7))),
  comorbidity = factor(sample(c("None", "Mild", "Severe"), n, replace = TRUE, prob = c(0.6, 0.3, 0.1))),
  outcome = rbinom(n, 1, prob = 0.3)
)

# Basic data exploration
cat("Dataset structure:\n")
print(glimpse(example_data))

# Summary statistics (without gtsummary)
cat("\nSummary statistics by treatment group:\n")
summary_stats <- example_data %>%
  group_by(treatment) %>%
  summarize(
    n = n(),
    age_mean = mean(age, na.rm = TRUE),
    age_sd = sd(age, na.rm = TRUE),
    bmi_mean = mean(bmi, na.rm = TRUE),
    bmi_sd = sd(bmi, na.rm = TRUE),
    male_pct = mean(sex == "Male", na.rm = TRUE) * 100,
    smoker_pct = mean(smoker == "Yes", na.rm = TRUE) * 100,
    outcome_pct = mean(outcome, na.rm = TRUE) * 100
  )
print(summary_stats)

# Example 2: Data visualization with ggplot2
# --------------------------------------------------

# Age distribution by treatment group
age_plot <- ggplot(example_data, aes(x = age, fill = treatment)) +
  geom_density(alpha = 0.5) +
  labs(
    title = "Age Distribution by Treatment Group",
    x = "Age (years)",
    y = "Density"
  ) +
  theme_minimal()

# Display plot information
cat("\nPlot created: Age Distribution by Treatment Group\n")
cat("To view this plot, run the following in R:\n")
cat("print(age_plot)\n\n")

# Outcome by treatment and comorbidity
outcome_data <- example_data %>%
  group_by(treatment, comorbidity) %>%
  summarize(outcome_rate = mean(outcome), .groups = "drop")

outcome_plot <- ggplot(outcome_data, aes(x = treatment, y = outcome_rate, fill = comorbidity)) +
  geom_col(position = "dodge") +
  labs(
    title = "Outcome Rate by Treatment and Comorbidity",
    x = "Treatment Group",
    y = "Outcome Rate",
    fill = "Comorbidity"
  ) +
  theme_minimal()

# Display plot information
cat("Plot created: Outcome Rate by Treatment and Comorbidity\n")
cat("To view this plot, run the following in R:\n")
cat("print(outcome_plot)\n\n")

# Example 3: Regression analysis
# --------------------------------------------------

# Logistic regression model
model <- glm(outcome ~ age + sex + treatment + bmi + smoker + comorbidity,
             family = binomial(link = "logit"),
             data = example_data)

# Model summary (without gtsummary)
cat("Logistic Regression Model Summary:\n")
model_summary <- summary(model)
print(model_summary)

# Calculate odds ratios and confidence intervals manually
cat("\nOdds Ratios and 95% Confidence Intervals:\n")
coefs <- coef(model_summary)
odds_ratios <- exp(coefs[, "Estimate"])
ci_lower <- exp(coefs[, "Estimate"] - 1.96 * coefs[, "Std. Error"])
ci_upper <- exp(coefs[, "Estimate"] + 1.96 * coefs[, "Std. Error"])
p_values <- coefs[, "Pr(>|z|)"]

or_table <- data.frame(
  OR = odds_ratios,
  CI_Lower = ci_lower,
  CI_Upper = ci_upper,
  p_value = p_values
)
print(or_table)

# Example 4: Propensity score analysis with WeightIt
# --------------------------------------------------

# Estimate propensity scores and weights
w_out <- weightit(treatment ~ age + sex + bmi + smoker + comorbidity,
                  data = example_data,
                  method = "ps",
                  estimand = "ATT")

# Examine balance
cat("\nPropensity Score Balance Summary:\n")
bal_table <- summary(w_out)
print(bal_table)

# Add weights to dataset
example_data$weights <- w_out$weights

# Weighted analysis
weighted_model <- glm(outcome ~ treatment,
                      family = binomial(link = "logit"),
                      data = example_data,
                      weights = weights)

# Weighted model summary
cat("\nWeighted Model Summary:\n")
weighted_summary <- summary(weighted_model)
print(weighted_summary)

# Calculate weighted odds ratios
cat("\nWeighted Odds Ratios and 95% Confidence Intervals:\n")
w_coefs <- coef(weighted_summary)
w_odds_ratios <- exp(w_coefs[, "Estimate"])
w_ci_lower <- exp(w_coefs[, "Estimate"] - 1.96 * w_coefs[, "Std. Error"])
w_ci_upper <- exp(w_coefs[, "Estimate"] + 1.96 * w_coefs[, "Std. Error"])
w_p_values <- w_coefs[, "Pr(>|z|)"]

w_or_table <- data.frame(
  OR = w_odds_ratios,
  CI_Lower = w_ci_lower,
  CI_Upper = w_ci_upper,
  p_value = w_p_values
)
print(w_or_table)

# Example 5: Data reshaping with tidyr
# --------------------------------------------------

# Create longitudinal data
long_data <- expand_grid(
  id = 1:100,
  visit = factor(1:4, levels = 1:4, labels = c("Baseline", "Month 3", "Month 6", "Month 12"))
) %>%
  mutate(
    treatment = rep(sample(c("Treatment A", "Treatment B"), 100, replace = TRUE), each = 4),
    age = rep(rnorm(100, mean = 50, sd = 15), each = 4),
    sex = rep(sample(c("Male", "Female"), 100, replace = TRUE), each = 4),
    measurement = rnorm(400, 
                        mean = case_when(
                          treatment == "Treatment A" & visit == "Baseline" ~ 10,
                          treatment == "Treatment A" & visit == "Month 3" ~ 9,
                          treatment == "Treatment A" & visit == "Month 6" ~ 8,
                          treatment == "Treatment A" & visit == "Month 12" ~ 7,
                          treatment == "Treatment B" & visit == "Baseline" ~ 10,
                          treatment == "Treatment B" & visit == "Month 3" ~ 9.5,
                          treatment == "Treatment B" & visit == "Month 6" ~ 9,
                          treatment == "Treatment B" & visit == "Month 12" ~ 8.5
                        ),
                        sd = 2)
  )

# Summarize longitudinal data
long_summary <- long_data %>%
  group_by(treatment, visit) %>%
  summarize(
    mean = mean(measurement),
    sd = sd(measurement),
    n = n(),
    se = sd / sqrt(n),
    .groups = "drop"
  )

cat("\nLongitudinal Data Summary:\n")
print(long_summary)

# Visualize longitudinal data
long_plot <- ggplot(long_summary, aes(x = visit, y = mean, group = treatment, color = treatment)) +
  geom_point(size = 3) +
  geom_line() +
  geom_errorbar(aes(ymin = mean - se, ymax = mean + se), width = 0.2) +
  labs(
    title = "Longitudinal Measurements by Treatment Group",
    x = "Visit",
    y = "Measurement",
    color = "Treatment"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Display plot information
cat("\nPlot created: Longitudinal Measurements by Treatment Group\n")
cat("To view this plot, run the following in R:\n")
cat("print(long_plot)\n\n")

# Print a message confirming the environment is set up correctly
cat("R environment is set up with ggplot2, dplyr, WeightIt, and tidyverse components.\n")
cat("This script demonstrates various statistical analyses for clinical epidemiology research.\n")
cat("Note: gtsummary could not be installed as it requires R 4.2+, but we have R 4.1.2.\n")
