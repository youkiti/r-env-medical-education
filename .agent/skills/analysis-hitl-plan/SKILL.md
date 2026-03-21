---
name: analysis-hitl-plan
description: Defines the human-in-the-loop analysis plan with numbered gates, variable definitions, model specs, assumption checks, and output agreements.
---

# Human-in-the-Loop Plan

- Draft the plan as an agreement document before implementation.

## Workflow Sequence and Gates

Execute in this exact order. Gates with formal approval requirement are marked with ✅.

```
Phase 0: Data Preparation
  ├─ Gate 0A: Environment Setup ✅
  └─ Gate 0B: Data Cleaning Plan ✅
Phase 1: Data Exploration
  └─ Gate 1: Exploration (no formal approval, proceed after visualization)
Phase 2: Data Analyses
  ├─ Gate 2A: Descriptive Statistics Plan ✅
  ├─ Gate 2B: Main Analysis Plan ✅ (includes assumption check agreement)
  ├─ Gate 2C: Sensitivity Analysis Plan ✅
  └─ Gate 2D: Exploratory Analysis Plan ✅
```

---

## Phase 0: Data Preparation

### Gate 0A: Environment Setup ✅

- Document R version and key package versions.
- List required packages and confirm availability.
- Specify data source and acquisition method.

### Gate 0B: Data Cleaning Plan ✅

> [!TIP]
> 実装の詳細は `data-wrangling` スキルを参照。

- Map variable names: list `names()` and `str()` and map to paper terms (e.g., MBP = MAP).
- Define inclusion/exclusion criteria with expected sample size at each step.
- Specify missing data handling rules.
- If custom functions are needed:
  - Define unit test cases (edge cases, missing data, boundary values).
  - Test functions before use in main analysis.
  - テスト実装は `tdd-testthat` スキルに従う。

---

## Phase 1: Data Exploration

### Gate 1: Exploration (承認不要)

- Generate distribution plots (histograms, bar charts) for all key variables.
- Generate bivariate relationship plots (scatterplots, boxplots).
- **No formal approval required.** Proceed to Phase 2 after generating visualizations.
- Document any unexpected patterns for discussion in Gate 2B.

---

## Phase 2: Data Analyses

### Gate 2A: Descriptive Statistics Plan ✅

- Define Table 1 structure: variables, stratification, summary statistics.
- Specify output format and file name.

### Gate 2B: Main Analysis Plan ✅

**Model Specification:**
- Specify the model as a formula with covariates.
- Define reference categories and coding.
- Specify outputs: file names, formats, and column order for tables; require PNG (300 dpi) plus PDF for figures.

**Assumption Check Agreement (Required vs Recommended):**

For each model type, pre-agree on:
1. **必須チェック**: 実施項目、判定基準、NG時の戻り先
2. **推奨チェック**: 実施トリガー（いつやるか）

| 区分 | 定義 | NG時の対応 |
|------|------|-----------|
| **必須** | 常に実施。NGなら解釈に進まない | Gate 2Bへ戻り、仕様を更新して再承認 |
| **推奨** | トリガー発生時のみ実施 | 原則Gate 2C（感度分析）へ回して頑健性を示す。重大なら Gate 2Bへ戻す |

### Gate 2C: Sensitivity Analysis Plan ✅

- Define sensitivity analysis criteria (e.g., outlier exclusion ±3SD).
- Specify alternative model specifications.
- Receive results from 推奨チェック that were triggered.
- Define expected comparison with main results.

### Gate 2D: Exploratory Analysis Plan ✅

- Define subgroup analyses (e.g., stratified by sex).
- List interaction terms to explore.
- Label all results as exploratory, not confirmatory.

---

## Model-Specific Assumption Checks

### Cox回帰

| 区分 | チェック項目 | 判定基準 | NG時の分岐例 |
|------|------------|---------|-------------|
| **必須** | `cox.zph()` + プロット（曝露・主要共変量） | p < 0.05 かつ視覚的に明確な傾向 | 時間依存効果を入れる / 層別化する / 追跡期間を区切る / 別指標(RMST)に切替 → Gate 2Bで選択理由を明記 |
| 推奨 | 連続共変量の関数形（スプライン比較） | — | Gate 2Cで結果を示す |
| 推奨 | 影響点（dfbeta等） | 極端な影響点の有無 | Gate 2Cで除外感度分析 |

### IPTW

| 区分 | チェック項目 | 判定基準 | NG時の分岐例 |
|------|------------|---------|-------------|
| **必須** | PSの重なり（分布プロット） | 両群で十分な重なり | 対象集団を限定 / マッチングに切替 → Gate 2Bで選択 |
| **必須** | 重み分布（min/max, 分位点, ESS） | 極端な重み（例: >10）がない | 重みトリミングを主解析に入れる / Gate 2Cで複数閾値の感度分析 → 事前に決定 |
| **必須** | バランス（SMD） | SMD < 0.1（目標） | PSモデル仕様を変更 → Gate 2Bへ戻る |
| 推奨 | トリミング閾値を変えた感度分析 | — | Gate 2Cで実施 |
| 推奨 | PSモデル仕様の代替 | — | Gate 2Cで実施 |
| 推奨 | 二重ロバスト（加重＋アウトカムモデル） | — | Gate 2Cで実施 |

### ロジスティック回帰

| 区分 | チェック項目 | 判定基準 | NG時の分岐例 |
|------|------------|---------|-------------|
| **必須** | アウトカム符号化の確認 | 0/1の意味が正しい | コーディング修正 → Gate 0Bへ戻る |
| **必須** | 収束・分離の確認（警告・推定値爆発） | 警告なし、係数が妥当な範囲 | Firth補正 / 変数除外 / ペナルティ付き回帰 → Gate 2Bで選択 |
| **必須** | 影響点の確認 | 極端な影響点がない | 除外感度分析をGate 2Cで実施 |
| 推奨 | 連続変数の線形性（スプライン比較、診断） | トリガー: 主要連続共変量が多い/外れ値疑い | Gate 2Cで結果を示す |
| 推奨 | 較正プロット | トリガー: 予測確率が0/1付近に張り付く | Gate 2Cで結果を示す |
| 推奨 | Hosmer–Lemeshow検定 | 必要時のみ | Gate 2Cで結果を示す |

### 線形回帰

| 区分 | チェック項目 | 判定基準 | NG時の分岐例 |
|------|------------|---------|-------------|
| **必須** | 線形性（ggplot2の診断図が可能なら優先、不可なら `plot(model, 1)`） | 残差に系統的パターンなし | 変換 / 非線形項追加 → Gate 2Bへ戻る |
| **必須** | 等分散性（ggplot2の診断図が可能なら優先、不可なら `plot(model, 3)`） | 残差の散らばりが一定 | 対数変換 / ロバストSE → Gate 2Bで選択 |
| **必須** | 残差正規性（ggplot2の診断図が可能なら優先、不可なら `plot(model, 2)`） | Q-Qプロットが概ね直線 | 大標本なら中心極限定理を根拠に進行可（記載必須） |
| 推奨 | 多重共線性 VIF（`car::vif()` 利用可能なら） | VIF < 5（目安） | Gate 2Cで変数除外感度分析 |

> [!NOTE]
> `car::vif()`, `survminer::ggcoxzph()` 等の追加パッケージは「利用可能なら実施」。
> 原則はggplot2での可視化を優先し、利用不可の場合は代替手順（base Rの`plot()`、手動計算など）で対応する。

---

## Small Sample Validation

- Run minimal sample or small subset first to validate variable names, formulas, and outputs.
- Compare basic counts (n, events, key proportions) to expected values and report differences.
- If discrepancies or spec changes arise, update the plan and re-approve before continuing.
- Do not suppress warnings globally; document any temporary warning changes with reasons.
