---
name: code-review-companion
description: Generates verification artifacts (back-translation, traceability, QA report, verification report) when outputting R scripts, enabling human review of AI-generated analysis code.
---

# Code Review Companion — Verification Artifact Skill

## Scope

- このスキルは verification artifact と verification file naming の正本。
- 一般的なスクリプト命名は `reproducibility-standards`、単体テスト命名は `tdd-testthat` が担当する。

AIがRスクリプトを出力する際、ヒトが検証するための **4つの検証アーティファクト** を段階的に生成する。

> [!IMPORTANT]
> 対象は `projects/` 配下のみ。トップレベル `scripts/` は変更しない。

## 段階分離

| 段階 | タイミング | 成果物 | 入力 |
|------|----------|--------|------|
| **Stage A** (静的) | スクリプト出力と同時 | 逆翻訳レポート, トレーサビリティ表 | コード内 `@plan_id` + `analysis_plan.md` |
| **Stage B** (実行後) | `run_all.R` → `99_verify_data.R` | QAレポート, 検証レポート | `qa_inputs.json` + `verification_config.yml` |

---

## Stage A: 静的検証（スクリプト出力時）

### 逆翻訳レポート (`back_translation.md`)

スクリプトを自然言語に再翻訳し、ユーザーが意図通りかを確認できるようにする。

- Rスクリプト出力と同時に生成
- セクションごとに `@plan_id` に基づくID参照を付与
- 出力先: `{project}/output/verification/back_translation.md`

### トレーサビリティ表 (`traceability_matrix.md`)

`analysis_plan.md` の各項目 → 実装コード行範囲のマッピング。

| 列 | 内容 |
|-----|------|
| Plan ID | `analysis_plan.md` の `G<gate>-<seq>` |
| Plan Description | 計画の記述 |
| Script | 実装スクリプトファイル名 |
| Line Range | `@plan_id` 開始行 〜 終端行 |
| Status | ✅ Implemented / ⚠ Partial / ❌ Missing |

- `analysis_plan.md` にIDがあるが `@plan_id` がどのスクリプトにもない → Status: ❌ Missing (Unimplemented Items)
- `@plan_id` に `analysis_plan.md` に存在しないIDがある → 警告を出力

出力先: `{project}/output/verification/traceability_matrix.md`

---

## Stage B: 実行後検証

### Stage B オーケストレーション

`run_all.R` の末尾で2つの処理を順に行う:

1. `qa_inputs.json` を `output/verification/` に書き出す
2. `source("99_verify_data.R")` を呼ぶ

```r
# run_all.R 末尾
# --- Stage B: Verification ---
cat(">>> Generating qa_inputs.json\n")
# ... (json書き出しコード) ...
cat(">>> Running verification\n")
source(file.path(project_root, "scripts", "99_verify_data.R"))
```

> `99_verify_data.R` は単独実行も可能（`qa_inputs.json` が既に存在する場合）。

### QAレポート (`qa_report.md`)

`verification_config.yml` の期待値と `qa_inputs.json` の実測値を突合し、結果を報告する。

出力先: `{project}/output/verification/qa_report.md`

### 検証レポート (`sample_verification_report.md`)

ファイル整合性チェック・Assumption Checks 結果を含む包括的な検証レポート。

出力先: `{project}/output/verification/sample_verification_report.md`

---

## パス規約

`{project}` = `projects/<analysis_name>/`。全パスは `{project}/` 基準。

### プロジェクトルート解決

`_project_config.R` をスクリプトフォルダに配置する。パス定義のみ、副作用なし。

```r
# scripts/_project_config.R （パス定義のみ、パッケージ読込・インストールなし）
project_root <- here::here("projects", "chatgpt_diagnostic_study")
output_dir   <- file.path(project_root, "output")
verify_dir   <- file.path(output_dir, "verification")
```

- `00_setup.R`: `source("_project_config.R")` した後にパッケージ読込等を行う
- `99_verify_data.R`: `source("_project_config.R")` のみで起動（パッケージ副作用なし）

### ディレクトリ構造

```
{project}/
├── analysis_plan.md
├── verification_config.yml
├── scripts/
│   ├── _project_config.R       ← パス定義のみ（副作用なし）
│   ├── 00_setup.R              ← source("_project_config.R") + パッケージ
│   ├── 01_data_import.R
│   ├── ...
│   ├── run_all.R               ← 末尾で qa_inputs.json 出力 + source("99_verify_data.R")
│   └── 99_verify_data.R        ← source("_project_config.R") のみ
└── output/
    └── verification/
        ├── back_translation.md       (Stage A)
        ├── traceability_matrix.md    (Stage A)
        ├── qa_inputs.json            (run_all.R が出力)
        ├── qa_report.md              (Stage B: 99_verify_data.R)
        └── sample_verification_report.md  (Stage B: 99_verify_data.R)
```

---

## `analysis_plan.md` のID規約

全項目に `G<gate>-<seq>` 形式のIDを付与する。

例: `G0-1`, `G1-3`, `G2-5`

## `@plan_id` タグ規約

Rスクリプト内のコメントタグ。コードブロックの対応先を示す。

```r
# @plan_id G1-3
some_analysis_code()
# @plan_id G1-4
next_analysis_code()
```

**終端規則**: 次の `@plan_id` タグ / `# ==` セパレータ / EOF のいずれか。

## `verification_config.yml`

`key_results` は `id+metric` 複合キーで一意。

```yaml
on_failure: warn   # warn | error
key_results:
  - id: G1-3
    metric: overall_accuracy
    expected: 0.765
    tolerance: 0.01
  - id: G1-3
    metric: n_cases
    expected: 36
    tolerance: 0
assumption_checks:
  - id: G2-1
    model: logistic_regression
    check: hoslem_test
    required: true
```

---

## `qa_inputs.json`

`run_all.R` 末尾でJSON出力。`key_results` は `[{id, metric, value}]` 配列。

```json
{
  "key_results": [
    {"id": "G1-3", "metric": "overall_accuracy", "value": 0.765},
    {"id": "G1-3", "metric": "n_cases", "value": 36}
  ],
  "assumption_checks": [
    {
      "id": "G2-1",
      "model": "logistic_regression",
      "check": "hoslem_test",
      "required": true,
      "result": "p = 0.45",
      "status": "pass"
    }
  ]
}
```

### key_results 突合ルール

Stage B で `verification_config.yml` と `qa_inputs.json` の `key_results` を `id+metric` で結合する際:

| 状況 | 判定 | 理由 |
|------|------|------|
| config にあって qa_inputs にない | **❌ FAIL** | 計画した検証が実行されていない |
| qa_inputs にあって config にない | **⚠ WARNING** (注記) | 想定外の指標。FAILにはしないが注記する |
| 両方にある → 通常の許容範囲判定 | ✅/❌ | tolerance で判定 |

### assumption_checks スキーマ

| フィールド | 型 | 必須 | 値域 |
|----------|-----|------|------|
| `id` | string | ✅ | `analysis_plan.md` のID |
| `model` | string | ✅ | |
| `check` | string | ✅ | |
| `required` | bool | ✅ | |
| `result` | string | ✅ | |
| `status` | string | ✅ | `"pass"` / `"fail"` / `"skipped"` |

**skipped の扱い**: `required + skipped` → ❌ FAIL / `recommended + skipped` → ✅ PASS (注記)

**スキーマ検証**: `99_verify_data.R` が読込時に必須フィールド・status値域を検証。不正 → ❌ FAIL。

---

## 検証失敗時の挙動

| `on_failure` | 動作 |
|-------------|------|
| `warn` | ❌ を記録。パイプライン完走 |
| `error` | 全レポートを書き切った後に `stop()` |

