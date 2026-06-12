# Simple demonstration of R packages for clinical epidemiology
# This script will run once the packages are installed

# Load required libraries
library(tidyverse)  # Data manipulation and visualization
library(ggplot2)    # Advanced plotting
library(dplyr)      # Data manipulation
library(gtsummary)  # Summary tables
library(WeightIt)   # Inverse probability weighting (alternative to iptw)

# Create a simple dataset
set.seed(123)
n <- 100
data <- tibble(
  id = 1:n,
  age = rnorm(n, mean = 50, sd = 15),
  sex = factor(sample(c("Male", "Female"), n, replace = TRUE)),
  treatment = factor(sample(c("A", "B"), n, replace = TRUE)),
  outcome = rbinom(n, 1, prob = ifelse(treatment == "A", 0.3, 0.5))
)

# Print dataset structure
cat("Dataset structure:\n")
print(glimpse(data))

# Create summary table with gtsummary
cat("\nSummary statistics by treatment group:\n")
tbl1 <- data %>%
  tbl_summary(
    by = treatment,
    include = c(age, sex, outcome)
  ) %>%
  add_p() %>%
  add_overall()
print(tbl1)

# Create visualization with ggplot2
p <- ggplot(data, aes(x = age, fill = treatment)) +
  geom_density(alpha = 0.5) +
  labs(title = "Age Distribution by Treatment Group")
print(p)

# Perform propensity score analysis with WeightIt
w <- weightit(treatment ~ age + sex, data = data, method = "ps")
bal <- summary(w)
cat("\nPropensity score balance summary:\n")
print(bal)

# Weighted analysis
weighted_model <- glm(outcome ~ treatment, 
                     family = binomial(link = "logit"),
                     data = data,
                     weights = w$weights)
cat("\nWeighted model summary:\n")
print(summary(weighted_model))

cat("\nAll packages loaded and demonstrated successfully!\n")
