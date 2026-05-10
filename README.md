# 臨床疫学研究のためのR環境

> **医学教育者向け fork (MMed 2026-05-13 ハンズオン用)**
> 親リポ [SRWS-PSG/r-environment-for-researcher](https://github.com/SRWS-PSG/r-environment-for-researcher) に、医学教育研究の練習プロジェクト [`projects/medical_education_admissions/`](projects/medical_education_admissions/) を追加した派生版です。
> 当日のハンズオンはそちらを使います (Table 1 / t検定 / χ² / 重回帰 を AI と Rmd で書く)。

本リポジトリは、AI（Antigravity / Gemini / Claudeなど）と一緒に臨床研究の統計解析を行うための環境です。
「AIに解析計画書を書かせる」「AIにRコードを書かせてコードをレビューする」といった作業をスムーズに行うための設定ファイルやデータがあらかじめ用意されています。

## どこに何があるか（ディレクトリ構造）

ハンズオン実習で迷わないよう、使うフォルダを以下にまとめました。

- `projects/`
  - 初心者向けの**実習用フォルダ**です。
  - 今回の実習では `projects/chatgpt_diagnostic_study/` を使用します。この中に論文PDF、テキスト化された論文(`paper.txt`)、および加工済みのダミーデータが入っています。
- `.agent/skills/`
  - **AIへの指示書（プロンプト）の集まり**です。
  - 実習で使う `sap-authoring`（解析計画書の作成）や、`code-review-companion`（出力されたコードの品質チェック）などが入っています。AIを研究アシスタントとして動かすための「呪文」のリストだと思ってください。
- `docs/`
  - マニュアルやガイドとなるドキュメントが入っています。
- `data/`
  - サンプルの生データが格納されています（今回はprojects内のデータを使用します）。

---

## ハンズオン用 環境セットアップの確認

事前に設定が終わっている場合は、GitHubから「クローン（Clone）」または最新のコミットを「Fetch」してあれば準備完了です。

**各種パッケージについて**
本リポジトリでは `renv` という仕組みを導入しており、解析に必要なパッケージが自動で同じバージョンに揃うようになっています（`renv.lock`ファイルで管理）。そのためエラーが起きにくくなっています。

---
---

# 【リファレンス】技術的な詳細とその他の使用例

> **Note**: 以下の内容は、さらに詳しい解析例や高度な設定情報を知りたい方向けのリファレンスです。実習中は特に読み込む必要はありません。

### インストール方法（コマンドラインから行う場合）

```bash
git clone https://github.com/SRWS-PSG/r-environment-for-researcher.git
cd r-environment-for-researcher

# renvでパッケージをインストール（全OS共通）
Rscript -e 'install.packages("renv"); renv::restore()'
```

### 含まれる主要パッケージ

| パッケージ | 用途 |
|------------|------|
| tidyverse | データ操作と可視化 |
| ggplot2 | 高度なデータ可視化 |
| dplyr | データ操作 |
| gtsummary | 統計表の作成（Table 1など） |
| WeightIt | IPTW（傾向スコア解析） |
| mice | 多重代入法（欠測データ処理） |
| survival | 生存分析（Kaplan-Meier、Cox回帰） |

### 統計原則のガイドライン

`principles/compiled_principles.md`ファイルには、臨床疫学研究における統計の原則がまとめられています。（STROBE statement、BMJ統計ガイドライン、JAMA著者向け指示）

### 高度な使用例

#### PLOS論文再現解析
`scripts/plos_analysis/`は、PLOS ONE論文の生存分析を再現する例です。Kaplan-Meier曲線、Cox回帰、Table 1の実装例が含まれています。

#### Zenodo時系列解析
`scripts/zenodo_analysis/`は、ECDCの病院・ICUデータを分析する実例です。回帰分析やWeightItを用いた傾向スコア解析、時系列予測モデルが含まれています。

### ライセンス

MIT
