# Bad example: uses random functions without set.seed()
# This violates reproducibility-standards

library(dplyr)
library(boot)

data <- read.csv("data/processed/analysis_data.csv")

# VIOLATION: sample() without prior set.seed()
train_idx <- sample(nrow(data), size = floor(0.8 * nrow(data)))
train <- data[train_idx, ]
test <- data[-train_idx, ]

# VIOLATION: rnorm() without prior set.seed()
noise <- rnorm(100, mean = 0, sd = 1)
