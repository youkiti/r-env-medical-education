# AIアシスタント向けガイド（臨床疫学R環境）

このリポジトリは、臨床疫学研究でよく使う統計解析をRで再現可能に実行するための環境と例を提供します。
このファイルは概要とスキルへの導線のみを記載します。詳細な手順・ガードレールは `.agent/skills/` を参照してください。

> [!IMPORTANT]
>
> AIは統計的に重要な判断を勝手に確定しないこと。選択肢とメリット・デメリットを示し、ユーザーの意図を確認して進める。

## リポジトリ構造（よく触る場所）

- `principles/`
- `docs/`
- `scripts/`
- `data/`

## まず参照するドキュメント（優先順）

1. `principles/compiled_principles.md`
2. `docs/r_usage_examples.md`
3. `docs/iptw_note.md`
4. `docs/troubleshooting.md`
5. `docs/summary.md`
6. `docs/r_environment_setup.md`
7. `docs/r_update_summary.md`

> [!NOTE]
>
> コマンド例はリポジトリ直下からの相対パスで記載しているため、必要に応じてカレントディレクトリをリポジトリのルートに合わせる。

## Skills (Antigravity)

### 解析の流れに沿ったスキルマップ

```
① analysis-intake          情報収集（研究目的・デザイン・変数）
       ↓
② sap-authoring            解析計画書（SAP）の作成 ★ NEW
       ↓
③ analysis-hitl-plan       Gate ID 付き実装計画
       ↓
④ data-wrangling           データ取得・クリーニング（Gate 0B）
       ↓
⑤ analysis-templates       既存テンプレート選択
       ↓
⑥ analysis-guardrails      統計ガードレール適用
       ↓
⑦ code-review-companion    検証アーティファクト生成
```

横断的に使うスキル: `output-and-naming-standards`, `tdd-testthat`, `causal-iptw-weightit`, `r-troubleshooting`, `data-privacy-handling`, `delegate-to-codex`

### スキル一覧

- `.agent/skills/analysis-intake/SKILL.md` - Collects study goals, design, variables, missingness, and reporting needs before starting clinical epidemiology analysis.
- `.agent/skills/sap-authoring/SKILL.md` - Generates a reproducibility-focused Statistical Analysis Plan (SAP) document with BMJ Open code-review framework, Decision log, and traceability to Gate IDs.
- `.agent/skills/data-wrangling/SKILL.md` - Guides data import, type conversion, missing data diagnosis, and cleaning for Gate 0B implementation.
- `.agent/skills/analysis-hitl-plan/SKILL.md` - Defines the human-in-the-loop analysis plan with data dictionary mapping, variable definitions, model specs, and output agreements.
- `.agent/skills/analysis-guardrails/SKILL.md` - Applies statistical guardrails, required checks, and non-negotiable prohibitions for clinical epidemiology analyses.
- `.agent/skills/analysis-templates/SKILL.md` - Selects and reuses existing scripts and docs as templates for common analysis types (descriptive, survival, IPTW, time series).
- `.agent/skills/output-and-naming-standards/SKILL.md` - Enforces output formats, file naming, workflow sequencing, coding style, and reproducibility conventions.
- `.agent/skills/causal-iptw-weightit/SKILL.md` - Guides IPTW with WeightIt, balance diagnostics, and stability checks for causal inference in observational data.
- `.agent/skills/r-troubleshooting/SKILL.md` - Triages R errors using reproducible steps, environment checks, and function disambiguation.
- `.agent/skills/data-privacy-handling/SKILL.md` - Handles sensitive data placement, git hygiene, and synthetic-data-first verification.
- `.agent/skills/tdd-testthat/SKILL.md` - testthat を用いたカスタムR関数のテスト駆動開発（TDD）手順・フィクスチャ・臨床データのエッジケースパターン。
- `.agent/skills/code-review-companion/SKILL.md` - Generates verification artifacts (back-translation, traceability, QA report, verification report) when outputting R scripts, enabling human review of AI-generated analysis code.
- `.agent/skills/delegate-to-codex/SKILL.md` - Launches OpenAI Codex CLI with context from current session to delegate coding tasks.

## SAP Workflow

解析計画書（SAP）を作成する際の流れ:

1. **情報収集**: `analysis-intake` で研究目的・デザイン・変数等を確認
2. **SAP 作成**: `sap-authoring` で BMJ Open 再現性フレームワークに基づく SAP を `{project}/docs/statistical_analysis_plan.md` に生成
3. **Gate 計画**: SAP の解析項目に Gate ID を付与し `analysis-hitl-plan` に沿って `analysis_plan.md` を生成
4. **実装 → 検証**: コード実装後、`code-review-companion` が SAP → コードのトレーサビリティを検証

参考: BMJ Open (PMC12496075) — 再現可能な解析コードの5提案

## Verification Workflow

Rスクリプトを `projects/` 配下に出力する際、`code-review-companion` スキルに従い検証アーティファクトを自動生成する。

1. **Stage A（静的）**: スクリプト出力と同時に逆翻訳レポート・トレーサビリティ表を `output/verification/` に生成
2. **Stage B（実行後）**: `run_all.R` が `qa_inputs.json` を書き出し、`99_verify_data.R` がQAレポート・検証レポートを生成

詳細は `.agent/skills/code-review-companion/SKILL.md` を参照。
