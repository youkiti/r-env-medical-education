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

- アウトカム（型：連続/二値/カウント/時間-to-イベント、測定タイミング、検閲の定義）
- 曝露/介入（群の定義、開始時点、時間依存の有無）
- 調整候補（交絡・共変量、事前に入れる変数の考え方）
- 変数のコード（0/1の意味、単位、異常値コード（例：999））

**欠測と除外**

- 欠測の量、欠測が起きる理由の見当、除外基準（完全ケース分析は原則推奨されにくいので要相談）

**報告形式**

- 効果指標（差/OR/RR/HR など）と、必ず95%CIも出すか
- 図表の希望（Table1、回帰表、KM曲線、バランスプロット等）

> [!TIP]

> ユーザーが迷っている場合は、まず「記述統計＋欠測要約＋簡単な可視化」までを先に作り、次にモデル化へ進める。

### 2) 実データを触る前の最低限チェック（勝手に省略しない）

-`n`（行数）と主要イベント数（アウトカムが二値/生存なら特に）

- 変数の型（数値/因子/日付）と単位
- 欠測のパターン（列ごとの欠測率、主要変数の欠測）
- あり得ない値（年齢<0、BMI極端、999等のコード）
- **イベント変数のカテゴリ（0/1/2/...の意味）を`table()`で確認**し、論文記載と対応づける

> [!CAUTION]
>
> **変数のコーディングを「推定」してコードを書かない**。イベント変数（status、event等）は必ず`table(df$status)`等で実際のカテゴリを確認し、論文記載の件数と照合してからコードに落とす。この手順を省略すると、生存解析等で全く異なる結果が出て、デバッグに時間を浪費する。

### 3) 必ずユーザー確認が必要な判断（例）

以下は結果が大きく変わり得るため、**選択肢を提示して確認**してください。

- 研究目的の分類（因果推論か、関連の記述か、予測か）
- 主要アウトカム/副次アウトカム、主要解析/感度解析の区別（多重比較の扱い）
- 欠測の扱い（完全ケースで進めるか、多重代入か、別法か）
- 連続変数の扱い（原則二値化しない；非線形を許すか等）
- クラスタリング/繰り返し測定の扱い（混合効果/ロバストSE等）
- 変数選択（p値だけで選ばない；原則は事前知識）
- 観察研究での因果効果の言い方（因果語を避ける/前提を明記）
- 傾向スコア法の推定対象（ATE/ATT）と、トリミング等のルール

### 4) デフォルトで進めてよい低リスク手順（ユーザーが未指定のとき）

- まずは `tbl_summary()` で全体/群別の記述統計（平均±SDやn(%)など）を作る
- 推定値＋95%CIを中心に整理し、p値だけの結論にしない（`principles/compiled_principles.md`参照）
- p値を示す場合は「P < 0.05」ではなく実値（例：`P = 0.043`）を使う
- 乱数を使う処理（サンプリング、分割、代入等）がある場合は `set.seed(123)` を明示
- 解析が重い/長い場合は、先に小さなサンプルで動作確認してから本番に進む
- 大規模データはメモリ使用量に注意し、列選択や集計から始める（`docs/summary.md`参照）

### 5) トラブルシューティング：最初の3手

- 実行コマンドとエラーメッセージ全文を確認（省略しない）

-`sessionInfo()`、`packageVersion()`、データの `str()`/`names()` で状況を切り分け

- 関数の衝突が疑わしい場合は `pkg::fun()` で明示（詳細は `docs/troubleshooting.md`）

## 因果推論（傾向スコア/IPTW）を扱うときの追加ガードレール

- このリポジトリでは `iptw` の代替として `WeightIt` を使用（`docs/iptw_note.md`）。

-**極端な傾向スコア（0/1付近）や極端な重み**が出る場合は、推定が不安定になりやすい：ユーザーに状況を報告し、トリミング等の選択肢を提示する（`docs/troubleshooting.md`にも例あり）。

-**バランス確認**（例：`WeightIt::summary()`、可能なら `cobalt` で `bal.tab()`/`love.plot()`）を必ず行い、結果（SMDなど）を添える。

- 観察研究では「因果効果」と言い切らない。前提（交絡の取り切れなさ等）を明記する（`principles/compiled_principles.md`参照）。

## 図の出力ルール（必須）

> [!IMPORTANT]

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

- 実行していない解析結果（数値・p値・図）を捏造しない
- 観察研究で因果を断定しない（言い回しと前提を明記）
- p値だけで結論を出さない（推定値＋CIを必ず併記）
