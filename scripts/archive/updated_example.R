# Updated example R script for clinical epidemiology analysis
# Using all requested packages: tidyverse, ggplot2, dplyr, gtsummary, WeightIt
# This script demonstrates statistical analysis techniques for clinical epidemiology research

# Load required libraries
library(tidyverse)  # Data manipulation and visualization
library(ggplot2)    # Advanced plotting
library(dplyr)      # Data manipulation
library(gtsummary)  # Statistical tables
library(WeightIt)   # Inverse probability weighting (alternative to iptw)

# Print R version and loaded package versions
cat("R Version:", R.version.string, "\n\n")
cat("Loaded packages:\n")
cat("---------------\n")
pkgs <- c("tidyverse", "ggplot2", "dplyr", "gtsummary", "WeightIt")
for(pkg in pkgs) {
  if(pkg %in% rownames(installed.packages())) {
    ver <- packageVersion(pkg)
    cat(sprintf("✓ %s version %s\n", pkg, ver))
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

# Example 2: Summary statistics with gtsummary
# --------------------------------------------------

# Create a summary table by treatment group using gtsummary
cat("\nCreating summary table with gtsummary...\n")
summary_table <- example_data %>%
  tbl_summary(
    by = treatment,
    include = c(age, sex, bmi, smoker, comorbidity, outcome),
    statistic = list(
      all_continuous() ~ "{mean} ({sd})",
      all_categorical() ~ "{n} ({p}%)"
    ),
    digits = all_continuous() ~ 1,
    label = list(
      age ~ "Age (years)",
      sex ~ "Sex",
      bmi ~ "BMI (kg/m²)",
      smoker ~ "Smoker",
      comorbidity ~ "Comorbidity",
      outcome ~ "Outcome"
    )
  ) %>%
  add_p() %>%
  add_overall() %>%
  bold_labels()

# Print the summary table
print(summary_table)

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

# Example 3: Regression analysis with gtsummary
# --------------------------------------------------

# Logistic regression model
model <- glm(outcome ~ age + sex + treatment + bmi + smoker + comorbidity,
             family = binomial(link = "logit"),
             data = example_data)

# Create a nice regression table with gtsummary
model_table <- tbl_regression(model, 
                             exponentiate = TRUE,
                             label = list(
                               age ~ "Age (years)",
                               sex ~ "Sex",
                               treatment ~ "Treatment",
                               bmi ~ "BMI (kg/m²)",
                               smoker ~ "Smoker",
                               comorbidity ~ "Comorbidity"
                             )) %>%
  add_global_p() %>%
  bold_p(t = 0.05) %>%
  bold_labels()

# Print the regression table
print(model_table)

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

# Create a nice weighted regression table with gtsummary
weighted_table <- tbl_regression(weighted_model, 
                                exponentiate = TRUE,
                                label = list(treatment ~ "Treatment (Weighted)")) %>%
  add_global_p() %>%
  bold_p(t = 0.05) %>%
  bold_labels()

# Print the weighted regression table
print(weighted_table)

# Example 6: Combining tables with gtsummary
# --------------------------------------------------

# Combine the unweighted and weighted models
combined_table <- tbl_merge(
  tbls = list(model_table, weighted_table),
  tab_spanner = c("**Unweighted Model**", "**Weighted Model**")
)

# Print the combined table
print(combined_table)

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

# Create a summary table for longitudinal data using gtsummary
long_table <- long_data %>%
  select(visit, treatment, measurement) %>%
  tbl_summary(
    by = visit,
    include = measurement,
    statistic = list(measurement ~ "{mean} ({sd})"),
    digits = measurement ~ 1,
    label = list(measurement ~ "Measurement")
  ) %>%
  add_p() %>%
  bold_labels()

# Print the longitudinal summary table
print(long_table)

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
cat("R environment is successfully set up with all requested packages:\n")
cat("- tidyverse for data manipulation and visualization\n")
cat("- ggplot2 for advanced plotting\n")
cat("- dplyr for data manipulation\n")
cat("- gtsummary for creating publication-ready tables\n")
cat("- WeightIt for inverse probability weighting (alternative to iptw)\n\n")
cat("This script demonstrates various statistical analyses for clinical epidemiology research.\n")
