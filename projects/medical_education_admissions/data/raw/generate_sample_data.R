# generate_sample_data.R
#
# 仮想データ (n=200) を生成して data/processed/sample.csv に保存する。
#
# モデル: Behnam et al. AMEP 2026 (Tehran TUMS, n=1,727)
#   "Admission Routes and Demographics as Predictors of Academic
#    Performance in Medical Students: A Retrospective Cohort of
#    GPAs and Comprehensive Exam Scores" DOI: 10.2147/AMEP.S574930
#
# 元論文の主な所見を再現する向きで生成パラメータを設定:
#   - 入学経路で gpa に差: General < Special < SemiSpecial < Olympiad
#   - cbse_repeat=1 の人は age が高めで gpa が低い
#   - entry_score は gpa の正の予測因子
#
# 実行:
#   Rscript projects/medical_education_admissions/data/raw/generate_sample_data.R
#
# 出力:
#   projects/medical_education_admissions/data/processed/sample.csv

set.seed(20260513)

n <- 200

admission_route <- sample(
  c("General", "Special", "SemiSpecial", "Olympiad"),
  size = n,
  replace = TRUE,
  prob = c(0.70, 0.10, 0.10, 0.10)
)

sex <- sample(c("M", "F"), size = n, replace = TRUE, prob = c(0.6, 0.4))

age_base <- rnorm(n, mean = 22, sd = 2)

route_age_offset <- c(
  General     = 0.0,
  Special     = 0.5,
  SemiSpecial = 0.5,
  Olympiad    = -1.0
)
age <- age_base + route_age_offset[admission_route]
age <- pmax(age, 18)
age <- round(age, 1)

route_entry_offset <- c(
  General     = 0.0,
  Special     = -3.0,
  SemiSpecial = -2.0,
  Olympiad    = 8.0
)
entry_score <- 70 + route_entry_offset[admission_route] + rnorm(n, 0, 8)
entry_score <- pmin(pmax(entry_score, 40), 100)
entry_score <- round(entry_score, 1)

route_gpa_offset <- c(
  General     = 0.0,
  Special     = 0.3,
  SemiSpecial = 0.5,
  Olympiad    = 1.2
)
gpa_linear <-
  15.5 +
  route_gpa_offset[admission_route] +
  0.04 * (entry_score - 70) +
  ifelse(sex == "F", 0.2, 0.0) +
  -0.05 * (age - 22) +
  rnorm(n, 0, 1.0)

gpa <- pmin(pmax(gpa_linear, 10), 20)
gpa <- round(gpa, 2)

cbse_repeat_logit <-
  -2.0 +
  -0.6 * route_gpa_offset[admission_route] +
  -0.05 * (entry_score - 70) +
  0.15 * (age - 22)
cbse_repeat_p <- 1 / (1 + exp(-cbse_repeat_logit))
cbse_repeat <- rbinom(n, size = 1, prob = cbse_repeat_p)

pass_cbse <- 1L - cbse_repeat

dat <- data.frame(
  id              = seq_len(n),
  age             = age,
  sex             = sex,
  admission_route = admission_route,
  entry_score     = entry_score,
  cbse_repeat     = as.integer(cbse_repeat),
  gpa             = gpa,
  pass_cbse       = as.integer(pass_cbse),
  stringsAsFactors = FALSE
)

out_dir <- file.path(
  "projects", "medical_education_admissions", "data", "processed"
)
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
out_path <- file.path(out_dir, "sample.csv")

write.csv(dat, out_path, row.names = FALSE)

cat(sprintf("Wrote %s (n=%d, %d cols)\n", out_path, nrow(dat), ncol(dat)))
cat("\n--- summary ---\n")
print(summary(dat))
cat("\n--- table(admission_route, cbse_repeat) ---\n")
print(table(dat$admission_route, dat$cbse_repeat))
