# Simple script to check which packages are already installed
installed_packages <- installed.packages()
cat("Currently installed R packages:\n")
cat("--------------------------------\n")
cat(paste(rownames(installed_packages), collapse=", "))
cat("\n\n")

# Check specifically for our required packages
required_packages <- c("tidyverse", "ggplot2", "dplyr", "gtsummary", "WeightIt")
for (pkg in required_packages) {
  if (pkg %in% rownames(installed_packages)) {
    cat(paste0("✓ Package '", pkg, "' is installed.\n"))
  } else {
    cat(paste0("✗ Package '", pkg, "' is NOT installed.\n"))
  }
}
