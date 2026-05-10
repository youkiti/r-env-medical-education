# generate_panel_data.R
#
# 仮想 IR (institutional research) パネルデータを生成して
# data/processed/ に 2 つの CSV を保存する。
#
# 出力:
#   - tums_panel.csv         : TUMS 単独 10 年パネル (ITS 用)
#   - multi_school_panel.csv : TUMS + University B 2 校 × 10 年パネル (DID 用)
#
# 想定 RQ:
#   2022 年度の新カリキュラム導入により、TUMS 医学生の
#   CBSE 一発合格率と GPA はどう変化したか?
#
# データ生成方針:
#   - 観察期間: 2017–2026 入学コホート (10 年)
#   - 介入時点: 2022 年 (TUMS のみ)
#   - 介入前 5 年は TUMS と UniB が緩く平行トレンド
#   - 2022 年に TUMS の mean_gpa が +0.5 水準ジャンプ + 緩い post-trend
#   - cbse_pass_rate は +0.05 (5pp) 水準ジャンプ + 緩い post-trend
#
# 実行:
#   Rscript projects/medical_education_panel/data/raw/generate_panel_data.R

set.seed(20260514)

years <- 2017:2026
n_years <- length(years)
intervention_year <- 2022

# 年度ごとのコホートサイズ (TUMS は ~150, UniB は ~140)
cohort_size_tums <- round(rnorm(n_years, mean = 150, sd = 8))
cohort_size_unib <- round(rnorm(n_years, mean = 140, sd = 8))

# ITS 用: time, intervention, time_after_intervention
time_idx <- seq_len(n_years)
intervention <- as.integer(years >= intervention_year)
time_after_intervention <- pmax(0L, years - intervention_year + 1L) * intervention

# ============================================================
# (1) TUMS 単独パネル (ITS 用)
# ============================================================
# モデル: mean_gpa = 16.40 + 0.00 * time
#                 + 0.50 * intervention                # 水準ジャンプ
#                 + 0.05 * time_after_intervention     # 介入後 slope
#                 + N(0, 0.05)                         # 年度集計の残差
mean_gpa_tums <-
  16.40 +
  0.00 * time_idx +
  0.50 * intervention +
  0.05 * time_after_intervention +
  rnorm(n_years, mean = 0, sd = 0.05)
mean_gpa_tums <- round(mean_gpa_tums, 2)

# CBSE 一発合格率 (proportion 0–1)
# モデル: 0.85 + 0.05 * intervention + 0.005 * time_after + N(0, 0.01)
cbse_pass_rate_tums <-
  0.85 +
  0.05 * intervention +
  0.005 * time_after_intervention +
  rnorm(n_years, mean = 0, sd = 0.01)
cbse_pass_rate_tums <- round(pmin(pmax(cbse_pass_rate_tums, 0), 1), 3)

tums_panel <- data.frame(
  year                    = years,
  cohort_size             = cohort_size_tums,
  mean_gpa                = mean_gpa_tums,
  cbse_pass_rate          = cbse_pass_rate_tums,
  intervention            = intervention,
  time                    = time_idx,
  time_after_intervention = time_after_intervention,
  stringsAsFactors        = FALSE
)

# ============================================================
# (2) TUMS + University B パネル (DID 用)
# ============================================================
# 介入校 = TUMS (treated=1)、対照校 = UniB (treated=0)
# UniB は介入を受けないので、TUMS と同じ baseline + 緩いトレンドのみ。
# TUMS 側は (1) と整合させる。

# UniB の mean_gpa: 16.30 + 0.00 * time + N(0, 0.05)
mean_gpa_unib <-
  16.30 +
  0.00 * time_idx +
  rnorm(n_years, mean = 0, sd = 0.05)
mean_gpa_unib <- round(mean_gpa_unib, 2)

cbse_pass_rate_unib <-
  0.83 +
  0.000 * time_idx +
  rnorm(n_years, mean = 0, sd = 0.01)
cbse_pass_rate_unib <- round(pmin(pmax(cbse_pass_rate_unib, 0), 1), 3)

# TUMS 側を再生成すると seed 進行で値がズレるので、(1) で作った値を流用する
multi_school_panel <- rbind(
  data.frame(
    year           = years,
    school         = "TUMS",
    cohort_size    = cohort_size_tums,
    mean_gpa       = mean_gpa_tums,
    cbse_pass_rate = cbse_pass_rate_tums,
    period         = ifelse(years >= intervention_year, "post", "pre"),
    treated        = 1L,
    stringsAsFactors = FALSE
  ),
  data.frame(
    year           = years,
    school         = "UniB",
    cohort_size    = cohort_size_unib,
    mean_gpa       = mean_gpa_unib,
    cbse_pass_rate = cbse_pass_rate_unib,
    period         = ifelse(years >= intervention_year, "post", "pre"),
    treated        = 0L,
    stringsAsFactors = FALSE
  )
)
# year, school でソート
multi_school_panel <- multi_school_panel[
  order(multi_school_panel$year, multi_school_panel$school),
]
rownames(multi_school_panel) <- NULL

# ============================================================
# 書き出し
# ============================================================
out_dir <- file.path(
  "projects", "medical_education_panel", "data", "processed"
)
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

tums_path <- file.path(out_dir, "tums_panel.csv")
multi_path <- file.path(out_dir, "multi_school_panel.csv")

write.csv(tums_panel, tums_path, row.names = FALSE)
write.csv(multi_school_panel, multi_path, row.names = FALSE)

cat(sprintf("Wrote %s (n=%d)\n", tums_path, nrow(tums_panel)))
cat(sprintf("Wrote %s (n=%d)\n", multi_path, nrow(multi_school_panel)))

cat("\n--- tums_panel.csv ---\n")
print(tums_panel)

cat("\n--- multi_school_panel.csv ---\n")
print(multi_school_panel)

# ============================================================
# 期待される ITS / DID 推定値 (sanity check)
# ============================================================
cat("\n--- ITS sanity check (TUMS, mean_gpa) ---\n")
its_fit <- lm(
  mean_gpa ~ time + intervention + time_after_intervention,
  data = tums_panel
)
print(summary(its_fit)$coefficients)

cat("\n--- DID sanity check (mean_gpa) ---\n")
# period を factor に
multi_school_panel$period <- factor(multi_school_panel$period, levels = c("pre", "post"))
multi_school_panel$school <- factor(multi_school_panel$school, levels = c("UniB", "TUMS"))
did_fit <- lm(
  mean_gpa ~ school + period + school:period,
  data = multi_school_panel
)
print(summary(did_fit)$coefficients)
