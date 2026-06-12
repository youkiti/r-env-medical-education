# Example R script for clinical epidemiology analysis
# Using tidyverse, ggplot2, dplyr, gtsummary, and WeightIt packages

# Load required libraries
library(tidyverse)  # Data manipulation and visualization
library(ggplot2)    # Advanced plotting
library(dplyr)      # Data manipulation
library(gtsummary)  # Summary tables
library(WeightIt)   # Inverse probability weighting

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
glimpse(example_data)

# Summary statistics using gtsummary
table1 <- example_data %>%
  tbl_summary(
    by = treatment,
    include = c(age, sex, bmi, smoker, comorbidity, outcome),
    statistic = list(
      all_continuous() ~ "{mean} ({sd})",
      all_categorical() ~ "{n} ({p}%)"
    ),
    digits = all_continuous() ~ 1
  ) %>%
  add_p() %>%
  add_overall() %>%
  bold_labels()

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

# Outcome by treatment and comorbidity
outcome_plot <- ggplot(example_data, aes(x = treatment, y = outcome, fill = comorbidity)) +
  stat_summary(fun = mean, geom = "bar", position = "dodge") +
  labs(
    title = "Outcome Rate by Treatment and Comorbidity",
    x = "Treatment Group",
    y = "Outcome Rate",
    fill = "Comorbidity"
  ) +
  theme_minimal()

# Example 3: Regression analysis
# --------------------------------------------------

# Logistic regression model
model <- glm(outcome ~ age + sex + treatment + bmi + smoker + comorbidity,
             family = binomial(link = "logit"),
             data = example_data)

# Model summary using gtsummary
model_table <- tbl_regression(model, exponentiate = TRUE) %>%
  add_global_p() %>%
  bold_p(t = 0.05) %>%
  bold_labels()

# Example 4: Propensity score analysis with WeightIt
# --------------------------------------------------

# Estimate propensity scores and weights
w_out <- weightit(treatment ~ age + sex + bmi + smoker + comorbidity,
                  data = example_data,
                  method = "ps",
                  estimand = "ATT")

# Examine balance
bal_table <- summary(w_out)

# Add weights to dataset
example_data$weights <- w_out$weights

# Weighted analysis
weighted_model <- glm(outcome ~ treatment,
                      family = binomial(link = "logit"),
                      data = example_data,
                      weights = weights)

# Weighted model summary
weighted_table <- tbl_regression(weighted_model, exponentiate = TRUE) %>%
  add_global_p() %>%
  bold_p(t = 0.05) %>%
  bold_labels()

# Example 5: Survival analysis
# --------------------------------------------------

# Create survival data
example_data$time <- rexp(n, rate = 0.1)
example_data$status <- rbinom(n, 1, 0.7)

# Kaplan-Meier curves
if (requireNamespace("survival", quietly = TRUE) && requireNamespace("survminer", quietly = TRUE)) {
  library(survival)
  library(survminer)
  
  # Create survival object
  surv_obj <- Surv(example_data$time, example_data$status)
  
  # Fit survival model
  km_fit <- survfit(surv_obj ~ treatment, data = example_data)
  
  # Plot Kaplan-Meier curves
  km_plot <- ggsurvplot(
    km_fit,
    data = example_data,
    risk.table = TRUE,
    pval = TRUE,
    conf.int = TRUE,
    xlab = "Time",
    ylab = "Survival Probability",
    title = "Kaplan-Meier Survival Curves by Treatment"
  )
}

# Example 6: Longitudinal data analysis
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

# Visualize longitudinal data
long_plot <- ggplot(long_data, aes(x = visit, y = measurement, group = treatment, color = treatment)) +
  stat_summary(fun = mean, geom = "point", size = 3) +
  stat_summary(fun = mean, geom = "line") +
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.2) +
  labs(
    title = "Longitudinal Measurements by Treatment Group",
    x = "Visit",
    y = "Measurement",
    color = "Treatment"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Mixed effects model for longitudinal data
if (requireNamespace("lme4", quietly = TRUE)) {
  library(lme4)
  
  # Fit mixed effects model
  mixed_model <- lmer(measurement ~ visit * treatment + age + sex + (1 | id), data = long_data)
  
  # Model summary
  mixed_summary <- summary(mixed_model)
}

# Save the example data for future use
# write_csv(example_data, "example_clinical_data.csv")
# write_csv(long_data, "example_longitudinal_data.csv")

# Print a message confirming the environment is set up correctly
cat("R environment is set up with tidyverse, ggplot2, dplyr, gtsummary, and WeightIt packages.\n")
cat("This script demonstrates various statistical analyses for clinical epidemiology research.\n")
