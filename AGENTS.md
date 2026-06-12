# AIアシスタント向けガイド（臨床疫学R環境）

> [!NOTE]
> このファイルは AI 向けの設定ファイルです。人間の利用者は [README.md](README.md) をご覧ください。

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
- `projects/`

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

このリポジトリでは、**13本のコアスキル**を `Core Workflow / Cross-cutting Controls / Method Skill` に分けて管理する。
`delegate-to-codex` はコア分析スキルではなく、補助的な Utility として扱う。

### Core Workflow

```text
① analysis-intake          情報収集と未確定事項の整理
       ↓
② sap-authoring            SAP 文書化
       ↓
③ analysis-hitl-plan       Gate ID 付き実装計画
       ↓
④ environment-setup        Gate 0A の実行環境確認
       ↓
⑤ data-wrangling           Gate 0B の実装
       ↓
⑥ analysis-implementation  projects/ 配下への実装展開
       ↓
⑦ code-review-companion    トレーサビリティと検証アーティファクト生成
```

### Cross-cutting Controls

- `analysis-guardrails`
- `reproducibility-standards`
- `data-privacy-handling`
- `tdd-testthat`
- `r-troubleshooting`

### Method Skill

- `causal-iptw-weightit`

### Utility

- `delegate-to-codex`

### スキル一覧

#### Core Workflow

- `.agent/skills/analysis-intake/SKILL.md` - Collects study goals, design, variables, missingness, reporting needs, and open decisions before planning starts.
- `.agent/skills/sap-authoring/SKILL.md` - Converts confirmed intake information into a Statistical Analysis Plan (SAP) and review checklist.
- `.agent/skills/analysis-hitl-plan/SKILL.md` - Converts an approved SAP into a Gate-based implementation plan with `G<gate>-<seq>` IDs.
- `.agent/skills/environment-setup/SKILL.md` - Establishes the executable R environment, package availability, paths, and Windows-safe runtime conventions.
- `.agent/skills/data-wrangling/SKILL.md` - Implements Gate 0B data import, type checks, missingness diagnosis, and cleaning rules.
- `.agent/skills/analysis-implementation/SKILL.md` - Maps an approved Gate plan into `projects/<analysis_name>/` structure and numbered scripts.
- `.agent/skills/code-review-companion/SKILL.md` - Generates verification artifacts (back-translation, traceability, QA report, verification report) for code review.

#### Cross-cutting Controls

- `.agent/skills/analysis-guardrails/SKILL.md` - Applies non-negotiable statistical rules and enforcement logic across analyses.
- `.agent/skills/reproducibility-standards/SKILL.md` - Defines naming, output, style, and session-recording conventions for reproducibility.
- `.agent/skills/data-privacy-handling/SKILL.md` - Handles sensitive data placement, git hygiene, and synthetic-data-first verification.
- `.agent/skills/tdd-testthat/SKILL.md` - Defines `testthat`-based TDD workflow, fixtures, and test file naming for custom R functions.
- `.agent/skills/r-troubleshooting/SKILL.md` - Triages R errors with reproducible steps, environment checks, and function disambiguation.

#### Method Skill

- `.agent/skills/causal-iptw-weightit/SKILL.md` - Owns IPTW-specific estimand, weighting, balance, and stability guidance using `WeightIt`.

#### Utility

- `.agent/skills/delegate-to-codex/SKILL.md` - Launches OpenAI Codex CLI with context from the current session to delegate coding tasks.

## スキル早引き表（初学者向け）

「どんな言葉で話しかけるとどのスキルが動くか」の対照表です。

| 話しかけ方の例 | 呼び出されるスキル |
|---|---|
| 「研究の目的は〜、デザインは〜」「変数を整理したい」 | `analysis-intake` |
| 「SAP を作りたい」「解析計画を文書化して」 | `sap-authoring` |
| 「実装計画を立てて」「Gate に分けて」 | `analysis-hitl-plan` |
| 「R環境を確認して」「パッケージが入っているか調べて」 | `environment-setup` |
| 「データを読み込んで」「欠損を確認して」「型を整えて」 | `data-wrangling` |
| 「Table 1 を作って」「回帰を実装して」「解析スクリプトを書いて」 | `analysis-implementation` |
| 「コードをレビューして」「SAP との整合を確認して」 | `code-review-companion` |
| 「エラーが出た」「パッケージが読み込めない」 | `r-troubleshooting` |
| 「因果関係を言いたい」「〜が〜を引き起こす、と書いていい？」 | `analysis-guardrails`（自動介入） |
| 「IPTWを使いたい」「重み付けの診断をして」 | `causal-iptw-weightit` |
| 「再現可能にしたい」「`renv` を使いたい」 | `reproducibility-standards` |
| 「患者データを扱う」「個人情報が含まれている」 | `data-privacy-handling` |
| 「テストを書きたい」「関数の動作を自動確認したい」 | `tdd-testthat` |

## Workflow Notes

### Planning Workflow

1. **情報収集**: `analysis-intake` で事実と未確定事項を収集する
2. **SAP 文書化**: `sap-authoring` で `{project}/docs/statistical_analysis_plan.md` を作成する
3. **Gate 化**: `analysis-hitl-plan` で `analysis_plan.md` に `G<gate>-<seq>` ID を付与する

### Execution Workflow

1. **環境確認**: `environment-setup` で Gate 0A を実施する
2. **データ整備**: `data-wrangling` で Gate 0B を実装する
3. **コード展開**: `analysis-implementation` で `projects/<analysis_name>/scripts/` に落とし込む
4. **検証**: `code-review-companion` で SAP → Plan → Code のトレーサビリティを検証する

### Verification Workflow

Rスクリプトを `projects/` 配下に出力する際、`code-review-companion` スキルに従い検証アーティファクトを生成する。

1. **Stage A（静的）**: スクリプト出力と同時に逆翻訳レポート・トレーサビリティ表を `output/verification/` に生成
2. **Stage B（実行後）**: `run_all.R` が `qa_inputs.json` を書き出し、`99_verify_data.R` が QA レポート・検証レポートを生成

詳細は `.agent/skills/code-review-companion/SKILL.md` を参照。
