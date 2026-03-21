source("_project_config.R")

cat("R version:", R.version.string, "\n")

required_packages <- c("dplyr", "ggplot2", "readxl", "pROC", "here")
for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    stop(paste("Package not available:", pkg))
  }
}

library(dplyr)
library(ggplot2)
library(readxl)
library(pROC)
library(here)

cat("All packages loaded successfully.\n")
cat("Session info saved.\n")
writeLines(capture.output(sessionInfo()), file.path(output_dir, "session_info.txt"))
