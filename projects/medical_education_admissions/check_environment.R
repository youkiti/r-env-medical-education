# check_environment.R
#
# 事前課題用：WS 当日に「動かない」を防ぐための動作確認スクリプト。
#
# 使い方（リポジトリルートで実行）:
#   source("projects/medical_education_admissions/check_environment.R")
#
# すべて [OK] が出れば WS 当日は問題なし。
# [MISSING] や [WARN] が出たら README.md の「ハマりどころ」表を参照。

required_pkgs <- c("rmarkdown", "knitr", "gtsummary", "dplyr", "broom", "ggplot2")

cat("\n========== Environment Check ==========\n")
cat(sprintf("R version    : %s\n", R.version.string))
cat(sprintf("Working dir  : %s\n", getwd()))
cat(sprintf("Platform     : %s\n", R.version$platform))

cat("\n--- 1. Packages ---\n")
missing_pkgs <- character(0)
for (p in required_pkgs) {
  ok <- requireNamespace(p, quietly = TRUE)
  status <- if (ok) "[OK]     " else "[MISSING]"
  ver <- if (ok) as.character(packageVersion(p)) else ""
  cat(sprintf("  %s %-12s %s\n", status, p, ver))
  if (!ok) missing_pkgs <- c(missing_pkgs, p)
}
if (length(missing_pkgs) > 0) {
  cat(sprintf("\n  -> Run: renv::restore()  # or install.packages(c(%s))\n",
              paste(sprintf('"%s"', missing_pkgs), collapse = ", ")))
}

cat("\n--- 2. Data file ---\n")
csv_path <- file.path("projects", "medical_education_admissions",
                      "data", "processed", "sample.csv")
if (file.exists(csv_path)) {
  dat <- tryCatch(
    read.csv(csv_path, fileEncoding = "UTF-8"),
    error = function(e) read.csv(csv_path)
  )
  cat(sprintf("  [OK]      Read %s\n", csv_path))
  cat(sprintf("            n = %d, cols = %d\n", nrow(dat), ncol(dat)))
  cat(sprintf("            columns: %s\n", paste(names(dat), collapse = ", ")))
} else {
  cat(sprintf("  [MISSING] %s\n", csv_path))
  cat("            -> Run: source(\"projects/medical_education_admissions/data/raw/generate_sample_data.R\")\n")
}

cat("\n--- 3. Pandoc (for knit to HTML) ---\n")
if (requireNamespace("rmarkdown", quietly = TRUE)) {
  if (rmarkdown::pandoc_available()) {
    cat(sprintf("  [OK]      pandoc %s\n",
                as.character(rmarkdown::pandoc_version())))
  } else {
    cat("  [WARN]    pandoc not found.\n")
    cat("            -> Knit from RStudio (RStudio bundles pandoc).\n")
    cat("               If running headless, install pandoc separately.\n")
  }
} else {
  cat("  [SKIP]    rmarkdown not installed; cannot check pandoc.\n")
}

cat("\n--- 4. Locale (Japanese display) ---\n")
loc <- Sys.getlocale("LC_CTYPE")
cat(sprintf("  LC_CTYPE = %s\n", loc))
if (grepl("UTF-?8|932|Japanese|ja_JP", loc, ignore.case = TRUE)) {
  cat("  [OK]      locale supports Japanese.\n")
} else {
  cat("  [WARN]    locale may not support Japanese plot labels.\n")
  cat("            -> If plots show garbled JP text, run:\n")
  cat("               Sys.setlocale(\"LC_CTYPE\", \"Japanese_Japan.utf8\")\n")
}

cat("\n========== Done ==========\n")
if (length(missing_pkgs) == 0 && file.exists(csv_path)) {
  cat("All required components present. You are ready for the workshop.\n\n")
} else {
  cat("Some components are missing. See messages above.\n\n")
}
