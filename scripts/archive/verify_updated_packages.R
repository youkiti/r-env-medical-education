# Verify installed packages after R update
cat("R Version Information:\n")
cat("---------------------\n")
print(R.version.string)
cat("\n")

# List of required packages
required_packages <- c("tidyverse", "ggplot2", "dplyr", "gtsummary", "WeightIt")

# Check which packages are installed
installed_pkgs <- installed.packages()
installed_names <- rownames(installed_pkgs)

cat("Package Installation Status:\n")
cat("--------------------------\n")
for (pkg in required_packages) {
  if (pkg %in% installed_names) {
    version <- installed_pkgs[pkg, "Version"]
    cat(sprintf("✓ %s (version %s) is installed\n", pkg, version))
  } else {
    cat(sprintf("✗ %s is NOT installed\n", pkg))
  }
}

cat("\nTrying to load packages:\n")
cat("----------------------\n")

# Try loading each package
for (pkg in required_packages) {
  if (pkg %in% installed_names) {
    tryCatch({
      cat(sprintf("Loading %s... ", pkg))
      library(pkg, character.only = TRUE)
      cat("SUCCESS\n")
    }, error = function(e) {
      cat(sprintf("FAILED: %s\n", e$message))
    })
  }
}

# For tidyverse, check component packages
if ("tidyverse" %in% installed_names) {
  cat("\nTidyverse component packages:\n")
  cat("---------------------------\n")
  tidyverse_pkgs <- c("readr", "tidyr", "purrr", "tibble", "stringr", "forcats")
  for (pkg in tidyverse_pkgs) {
    if (pkg %in% installed_names) {
      version <- installed_pkgs[pkg, "Version"]
      cat(sprintf("✓ %s (version %s) is installed\n", pkg, version))
    } else {
      cat(sprintf("✗ %s is NOT installed\n", pkg))
    }
  }
}

# Note about WeightIt as alternative to iptw
cat("\nNote: WeightIt package is used as an alternative to iptw for inverse probability weighting.\n")
cat("WeightIt provides more flexible and comprehensive functionality for propensity score analysis.\n")

# Session info
cat("\nSession Information:\n")
cat("-------------------\n")
print(sessionInfo())
