---
name: tdd-testthat
description: testthat を用いたカスタムR関数のテスト駆動開発（TDD）手順・フィクスチャ・臨床データのエッジケースパターン。
---

# TDD with testthat

- TDDの核: 先に失敗するテストを書く → 最小実装で通す → 安全にリファクタする。
- 対象: `utils_*.R` に切り出すカスタム関数（データクリーニング、計算ヘルパー、バリデーション等）。
- 番号付きスクリプト（`01_*.R` 等）自体はテスト対象外。パイプラインの正しさは `code-review-companion` の検証アーティファクトで担保する。

## `utils_*.R` のルール

> [!CAUTION]
> `utils_*.R` は**純粋な関数定義のみ**を含むこと（副作用なし）。
> - ✅ 関数定義 (`foo <- function(...) { ... }`)
> - ❌ `library()` / `require()` の呼び出し
> - ❌ ファイルI/O（`read.csv`, `saveRDS` 等）の直接実行
> - ❌ グローバル変数への代入
> - ❌ `source()` のネスト
>
> これにより、テストランナーでの一括 `source()` が安全になる。
> `_project_config.R` の「パス定義のみ・副作用なし」と同じ原則。

## `@plan_id` との関係

`@plan_id` は番号付きスクリプト（呼び出し元）に付与する。`utils_*.R` には付けない。

トレーサビリティ表（`code-review-companion`）は呼び出し元スクリプトを正本とする。`utils_*.R` は「テスト済みの部品」として信頼し、呼び出し箇所でトレーサビリティを確保する。

```r
# 03_primary_analysis.R
source("scripts/utils_clean_data.R")  # テスト済み関数

# @plan_id G2B-1
df_clean <- clean_sentinel(df$age, sentinel = 999)
result   <- calc_bmi(df_clean$weight, df_clean$height)
```

---

## TDD サイクル（Red → Green → Refactor）

### 1モジュール = 1テストペアの原則

| 実装ファイル | テストファイル | 説明 |
|-------------|-------------|------|
| `utils_clean_data.R` | `test-clean_data.R` | データクリーニング関数群 |
| `utils_calc_metrics.R` | `test-calc_metrics.R` | 計算ヘルパー関数群 |
| `utils_validate.R` | `test-validate.R` | バリデーション関数群 |

命名対応ルール: `utils_<module>.R` → `test-<module>.R`

### 実行手順（devtools 非依存）

> [!IMPORTANT]
> この環境には `devtools` がインストールされていない。`source()` + `testthat::test_file()` を使用する。

```r
# 1. 関数を読み込む
source("scripts/utils_clean_data.R")

# 2. 単一テストファイルを実行（Red → Green の繰り返し）
testthat::test_file("tests/testthat/test-clean_data.R")

# 3. 全テストを実行（Refactor 後の確認）
testthat::test_dir("tests/testthat/")
```

### サイクルの流れ

1. **Red**: `test-<module>.R` にまだ存在しない関数のテストを書く → 実行して失敗を確認
2. **Green**: `utils_<module>.R` に最小実装を書く → `source()` で再読込 → `test_file()` で通す
3. **Refactor**: テストが通った状態でコードを整理 → `test_dir()` で全テスト通過を確認

---

## ディレクトリ構造とファイル命名

```
{project}/
├── scripts/
│   ├── _project_config.R           ← パス定義のみ（副作用なし）
│   ├── utils_clean_data.R          ← テスト対象の関数（副作用なし）
│   ├── utils_calc_metrics.R
│   ├── 01_import_data.R
│   ├── 03_primary_analysis.R       ← source() + @plan_id
│   └── ...
├── tests/
│   ├── testthat.R                  ← テストランナー
│   └── testthat/
│       ├── helper-test_data.R      ← テスト用共通データ（任意）
│       ├── test-clean_data.R
│       └── test-calc_metrics.R
└── ...
```

### テストランナー（`tests/testthat.R`）

```r
# tests/testthat.R
# プロジェクトルートから実行: source("tests/testthat.R")

project_root <- here::here("projects", "<analysis_name>")
scripts_dir  <- file.path(project_root, "scripts")
tests_dir    <- file.path(project_root, "tests", "testthat")

# utils_*.R を一括読み込み（副作用なしの関数定義のみ）
utils_files <- list.files(scripts_dir, pattern = "^utils_.*\\.R$", full.names = TRUE)
for (f in utils_files) source(f)

# テスト実行
testthat::test_dir(tests_dir, reporter = testthat::default_reporter())
```

### ファイル命名規約

| パターン | ファイル名 | 場所 |
|---------|-----------|------|
| 実装 | `utils_<module>.R` | `scripts/` |
| テスト | `test-<module>.R` | `tests/testthat/` |
| ヘルパー | `helper-<name>.R` | `tests/testthat/` |
| フィクスチャ | `<name>.rds` | `tests/testthat/_fixtures/` |

> [!NOTE]
> `output-and-naming-standards` の `utils_<function>.R` 命名規約に準拠。

---

## テストファイルの基本構造

```r
# tests/testthat/test-clean_data.R

test_that("clean_sentinel replaces sentinel with NA", {
  x <- c(25, 999, 40, 999)
  result <- clean_sentinel(x, sentinel = 999)
  expect_equal(result, c(25, NA, 40, NA))
})

test_that("clean_sentinel handles multiple sentinels", {
  x <- c(25, 999, -1, 40)
  result <- clean_sentinel(x, sentinel = c(999, -1))
  expect_equal(result, c(25, NA, NA, 40))
})
```

---

## フィクスチャパターン（withr）

テストの独立性を保つため、`withr::local_*()` でグローバル状態を一時的に変更する。テスト終了時に自動的に元に戻る。

> [!TIP]
> `withr::local_*()` は `with_*()` より推奨。`local_*()` は `test_that()` ブロック終了時に自動クリーンアップされる。

### オプション変更

```r
test_that("scipen で科学的記数法を抑制した状態でフォーマット", {
  withr::local_options(list(scipen = 999))
  result <- format_pvalue(0.00001)
  expect_equal(result, "0.00001")
})
```

### 一時ファイル・ディレクトリ

```r
test_that("CSVエクスポートが正しく動作する", {
  tmp_dir <- withr::local_tempdir()
  export_table1(df, output_dir = tmp_dir)
  expect_true(file.exists(file.path(tmp_dir, "table1.csv")))
})
```

### シード固定

```r
test_that("ブートストラップCIが再現可能", {
  withr::local_seed(123)
  ci <- bootstrap_ci(data, n_boot = 100)
  expect_length(ci, 2)
  expect_true(ci[1] < ci[2])
})
```

### 環境変数

```r
test_that("環境変数からパスを取得", {
  withr::local_envvar(DATA_DIR = withr::local_tempdir())
  path <- get_data_path()
  expect_true(dir.exists(dirname(path)))
})
```

---

## モックパターン

外部依存（ファイルI/O、API、日付）をモックに置き換えてテストする。

> [!CAUTION]
> 旧APIの `testthat::with_mock()` は非推奨。`testthat::local_mocked_bindings()` を使う。

```r
test_that("fetch_patient_count uses API result", {
  local_mocked_bindings(
    api_get = function(endpoint) list(count = 42)
  )
  result <- fetch_patient_count("cohort_a")
  expect_equal(result, 42)
})
```

### モックが有効な場面

| 場面 | モック対象 | 理由 |
|------|----------|------|
| プライベートデータ読込 | `read.csv`, `readRDS` | 実データなしでテスト可能 |
| 外部API | `httr::GET` | ネットワーク不要 |
| 日付依存処理 | `Sys.Date`, `Sys.time` | 再現可能 |
| ランダム処理 | `sample`, `rnorm` | 決定論的テスト（`withr::local_seed` でも可） |

> [!TIP]
> `data-privacy-handling` の原則に従い、テストでは実データではなく合成データを使う。

---

## パラメタライズドテスト（Table-Driven）

同じ関数を多くの入力パターンでテストする場合、テーブル駆動方式でケースを列挙する。

```r
test_that("calc_bmi works for multiple cases", {
  cases <- list(
    list(weight = 70,  height = 1.75, expected = 22.86, label = "normal"),
    list(weight = 50,  height = 1.60, expected = 19.53, label = "low-normal"),
    list(weight = 120, height = 1.80, expected = 37.04, label = "obese"),
    list(weight = NA,  height = 1.75, expected = NA_real_, label = "weight NA"),
    list(weight = 70,  height = NA,   expected = NA_real_, label = "height NA"),
    list(weight = 70,  height = 0,    expected = NA_real_, label = "height zero")
  )

  for (tc in cases) {
    expect_equal(
      calc_bmi(tc$weight, tc$height), tc$expected,
      tolerance = 0.01, label = tc$label
    )
  }
})
```

> [!TIP]
> `label` 引数を使うと、失敗時にどのケースで落ちたかが明確になる。

---

## 臨床疫学データの典型的テストケース

### 欠損データ（NA）

```r
test_that("NA handling: partial, all, none", {
  # 一部NA
  expect_equal(calc_complete_rate(c(1, NA, 3)), 2/3)
  # 全NA
  expect_equal(calc_complete_rate(c(NA_real_, NA_real_)), 0)
  # NAなし
  expect_equal(calc_complete_rate(c(1, 2, 3)), 1)
})
```

### センチネル値

```r
test_that("sentinel values: 999, -1, empty string", {
  expect_equal(clean_sentinel(c(25, 999), sentinel = 999), c(25, NA))
  expect_equal(clean_sentinel(c(1, -1), sentinel = -1), c(1, NA))
  expect_equal(clean_sentinel_char(c("Y", ""), sentinel = ""), c("Y", NA))
})
```

### 境界値・空入力

```r
test_that("boundary: zero, negative, extreme", {
  expect_false(is_valid_bmi(0))
  expect_false(is_valid_bmi(-1))
  expect_false(is_valid_bmi(100))
  expect_true(is.na(is_valid_bmi(NA)))
})

test_that("empty input: 0-row data.frame", {
  df <- data.frame(age = numeric(0))
  result <- calc_complete_rate_df(df)
  expect_equal(nrow(result), 0)
})
```

### エッジケースチェックリスト

テストケースを設計する際、以下を体系的に確認する:

| カテゴリ | テストすべきケース | 例 |
|---------|-----------------|-----|
| 欠損 | 全NA、一部NA、NAなし | `c(NA, NA)`, `c(1, NA, 3)`, `c(1, 2, 3)` |
| センチネル | 999, -1, -9, 空文字, "NA"文字列 | `c(25, 999)`, `c("Y", "")` |
| 境界 | 0、負値、極端な大値 | age=0, BMI=100, weight=-1 |
| 空入力 | 0行、0列、NULL | `data.frame()`, `NULL` |
| 型 | numeric, character, factor, Date | `as.Date("2024-01-01")` |
| 一行 | n=1のケース | 単一行データフレーム |
| 重複 | 完全重複行 | `rbind(row, row)` |

---

## スナップショットテスト

テーブル出力や長い文字列の回帰テストに使う。初回実行時にスナップショットを保存し、以後の実行で差分を検出する。

> [!CAUTION]
> Windows + PowerShell 環境では日本語出力がCP932で壊れる可能性がある。
> `expect_snapshot()` は**ロケール非依存な英語出力のみ**に使用する。
> `output-and-naming-standards` の Windows encoding rules に従うこと。

```r
test_that("summary table output is stable", {
  df <- create_test_cohort()  # helper-test_data.R で定義
  result <- generate_summary(df)
  expect_snapshot(print(result))
})

test_that("CSV export content is stable", {
  tmp <- withr::local_tempfile(fileext = ".csv")
  export_results(test_data, path = tmp)
  expect_snapshot_file(tmp, name = "results.csv")
})
```

> [!NOTE]
> スナップショットは `tests/testthat/_snaps/` に保存される。Git で追跡すること。
> 意図的な出力変更時は `testthat::snapshot_accept()` で更新する。

---

## カバレッジ（任意）

> [!NOTE]
> `covr` は現在 renv に直接インストールされていない。必要な場合はユーザーに確認の上インストールする。

```r
if (requireNamespace("covr", quietly = TRUE)) {
  cov <- covr::file_coverage(
    source_files = "scripts/utils_clean_data.R",
    test_files   = "tests/testthat/test-clean_data.R"
  )
  print(cov)
  # covr::report(cov)  # HTMLレポート生成
}
```

---

## 他スキルとの連携

| 連携先スキル | 連携内容 |
|------------|---------|
| `analysis-guardrails` | カスタム関数のユニットテスト要件 → このスキルで実装 |
| `analysis-hitl-plan` | Gate 0B でのテストケース定義 → このスキルで実装 |
| `analysis-intake` | ユニットテスト要否の確認 → 「はい」ならこのスキルを適用 |
| `code-review-companion` | `@plan_id` は呼び出し元スクリプトに付与。`utils_*.R` はテスト済み部品として信頼 |
| `output-and-naming-standards` | `utils_<module>.R` 命名規約に準拠。テストファイル命名は `test-<module>.R` |
| `data-privacy-handling` | テストデータに実データを使わない。合成データを使用 |
| `sap-authoring` | SAP §13 のユニットテスト計画と整合 |

## 注意事項

- テストデータに実データを使わないこと（`data-privacy-handling` 参照）。
- Windows パス問題は `here::here()` + `file.path()` で回避する。
- `utils_*.R` が多数（目安5個超）になった場合、内部パッケージ化を検討する。
