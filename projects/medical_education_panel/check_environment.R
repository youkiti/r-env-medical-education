# check_environment.R
#
# Day 2 (準実験法各論) ハンズオン用の動作確認スクリプト。
# Day 1 の `medical_education_admissions/check_environment.R` と同じ趣旨で、
# パネル CSV 2 つの読み込みまで確認する。
#
# 使い方 (リポジトリルートで実行):
#   source("projects/medical_education_panel/check_environment.R")
#
# すべて [OK] が出れば Day 2 のハンズオンは問題なし。

required_pkgs <- c("rmarkdown", "knitr", "gtsummary", "dplyr", "broom", "ggplot2")

cat("\n========== Environment Check (Day 2: Panel) ==========\n")
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

cat("\n--- 2. Data files ---\n")
panel_dir <- file.path("projects", "medical_education_panel", "data", "processed")
files_to_check <- list(
  list(
    path = file.path(panel_dir, "mmed_panel.csv"),
    expected_cols = c("year", "cohort_size", "mean_gpa", "cbse_pass_rate",
                      "intervention", "time", "time_after_intervention"),
    expected_n = 10
  ),
  list(
    path = file.path(panel_dir, "multi_school_panel.csv"),
    expected_cols = c("year", "school", "cohort_size", "mean_gpa",
                      "cbse_pass_rate", "period", "treated"),
    expected_n = 20
  )
)

all_data_ok <- TRUE
for (f in files_to_check) {
  if (file.exists(f$path)) {
    dat <- tryCatch(
      read.csv(f$path, fileEncoding = "UTF-8"),
      error = function(e) read.csv(f$path)
    )
    cols_ok <- all(f$expected_cols %in% names(dat))
    n_ok <- nrow(dat) == f$expected_n
    if (cols_ok && n_ok) {
      cat(sprintf("  [OK]      %s\n", f$path))
      cat(sprintf("            n = %d, cols = %d\n", nrow(dat), ncol(dat)))
    } else {
      cat(sprintf("  [WARN]    %s\n", f$path))
      cat(sprintf("            n = %d (expected %d), cols ok = %s\n",
                  nrow(dat), f$expected_n, cols_ok))
      all_data_ok <- FALSE
    }
  } else {
    cat(sprintf("  [MISSING] %s\n", f$path))
    cat("            -> Run: source(\"projects/medical_education_panel/data/raw/generate_panel_data.R\")\n")
    all_data_ok <- FALSE
  }
}

cat("\n--- 3. Pandoc (for knit to HTML) ---\n")
if (requireNamespace("rmarkdown", quietly = TRUE)) {
  if (rmarkdown::pandoc_available()) {
    cat(sprintf("  [OK]      pandoc %s\n",
                as.character(rmarkdown::pandoc_version())))
  } else {
    cat("  [WARN]    pandoc not found.\n")
    cat("            -> Knit from RStudio (RStudio bundles pandoc).\n")
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
if (length(missing_pkgs) == 0 && all_data_ok) {
  cat("All required components present. You are ready for Day 2.\n\n")
} else {
  cat("Some components are missing. See messages above.\n\n")
}
