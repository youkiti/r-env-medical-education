# ChatGPT Diagnostic Accuracy Study - ハンズオン演習

## 🎯 目的

この演習では、PLOS ONE論文の解析をRで再現することで、臨床研究データ解析の基礎スキルを身につけます。

## 📄 論文情報

- **タイトル**: Evaluation of ChatGPT as a diagnostic tool for medical learners and clinicians
- **DOI**: [10.1371/journal.pone.0307383](https://doi.org/10.1371/journal.pone.0307383)
- **掲載誌**: PLOS ONE
- **概要**: ChatGPT（大規模言語モデル）の診断精度を150のMedscapeケースチャレンジを用いて評価した研究

## 📊 論文の主要な知見（これを再現するのがゴール）

| 指標 | 論文の結果 |
|------|-----------|
| 正答率 (Case Accuracy) | 49.3% (74/150) |
| Overall Accuracy | 74% |
| Precision | 48.67% |
| Sensitivity | 48.67% |
| Specificity | 82.89% |
| AUC | 0.66 |

**認知負荷 (Cognitive Load)**
- Low: 77 (51%)
- Moderate: 61 (41%)
- High: 11 (7%)

**医学情報の品質 (Quality of Medical Information)**
- Complete/Relevant: 78 (52%)
- Incomplete/Relevant: 64 (43%)
- Incomplete/Irrelevant: 8 (5%)

## 📁 ディレクトリ構成

```
chatgpt_diagnostic_study/
├── data/
│   └── processed/        # 解析用データ（ここから始める）
│       ├── chatgpt_cases_cleaned.csv      # メインデータ (150ケース)
│       ├── diagnostic_accuracy_600.csv    # 診断精度データ (600レスポンス)
│       └── all_reviews.csv                # レビュアーデータ
├── docs/                 # 論文テキスト（参考用）
├── scripts/              # ← ここに自分でスクリプトを書く！
├── output/
│   ├── figures/          # 生成した図を保存
│   └── tables/           # 生成した表を保存
└── README.md
```

## 🚀 演習の進め方

### Step 1: データの確認
```r
library(tidyverse)
cases <- read_csv("data/processed/chatgpt_cases_cleaned.csv")
glimpse(cases)
```

### Step 2: Primary Outcome（正答率）を計算
```r
# ヒント: answer_correct_bool列を使う
# 目標: 74/150 = 49.3%
```

**AIへの頼み方（例）:**
```
このリポジトリの projects/chatgpt_diagnostic_study/data/processed/chatgpt_cases_cleaned.csv を
読み込んで、answer_correct_bool 列から正答率 (Accuracy) を計算する R コードを書いてください。
目標値は 74/150 = 49.3% です。R 初心者なので各行にコメントを付けてください。
```

### Step 3: 診断精度指標を計算
```r
# ヒント: diagnostic_accuracy_600.csv を使う
# TP, FP, TN, FN を数えて、Accuracy, Precision, Sensitivity, Specificity を計算
```

**AIへの頼み方（例）:**
```
projects/chatgpt_diagnostic_study/data/processed/diagnostic_accuracy_600.csv を読み込んで、
diagnostic_result列 (True Positive/False Positive/True Negative/False Negative) の件数から
TP, FP, TN, FN を数え、Accuracy, Precision, Sensitivity, Specificity を計算する R コードを
書いてください。pROC パッケージを使って AUC も計算してください。
目標値は Accuracy 74%、Sensitivity 48.67%、Specificity 82.89%、AUC 0.66 です。
R 初心者なので各行にコメントを付けてください。
```

### Step 4: 図を作成
- Figure 1: 正答/誤答の棒グラフ
- Figure 2: 混同行列（ヒートマップ）
- Figure 3: ROC曲線
- Figure 4: 認知負荷の分布
- Figure 5: 医学情報品質の分布

**AIへの頼み方（例）:**
```
chatgpt_cases_cleaned.csv と diagnostic_accuracy_600.csv を使って、次の5つの図を
ggplot2 で作成する R コードを書いてください。
1. 正答/誤答の棒グラフ
2. 混同行列のヒートマップ (geom_tile を使う)
3. ROC曲線 (pROCパッケージを使う)
4. cognitive_load_std (認知負荷) の分布
5. quality_answer_std (医学情報の品質) の分布
図はそれぞれ output/figures/ 以下に ggsave() で保存してください。
R 初心者なので各行にコメントを付けてください。
```

### Step 5: 結果を論文と比較
自分の結果が論文の値と一致しているか確認する

## 📦 データ説明

### chatgpt_cases_cleaned.csv（メインデータ）
| 列名 | 説明 |
|-----|------|
| case_id | ケースID (1-150) |
| case_name | ケース名 |
| answer_correct | 正答かどうか ("yes"/"no") |
| answer_correct_bool | 正答かどうか (TRUE/FALSE) |
| cognitive_load_std | 認知負荷 (Low/Moderate/High) |
| quality_answer_std | 医学情報の品質 |

### diagnostic_accuracy_600.csv（診断精度データ）
| 列名 | 説明 |
|-----|------|
| response_id | レスポンスID (1-600) |
| case_id | ケースID |
| option | 選択肢番号 (1-4) |
| diagnostic_result | 結果 (True Positive/False Positive/True Negative/False Negative) |

## 💡 ヒント

1. **ggplot2**でグラフを作成する
2. **dplyr**のcount(), summarise()で集計する
3. 混同行列はgeom_tile()で描ける
4. AUCの計算には**pROC**パッケージが便利

## 📝 提出物

1. scripts/以下に作成したRスクリプト
2. output/figures/以下に生成した図
3. output/tables/以下に生成した表

---

> **Note**: 元論文の生データは構造が複雑なため、解析しやすいように `scripts/00_generate_synthetic_data.R` を使って論文の報告値に基づく合成データ（実習用データ）を生成しています。実際の解析手法を学ぶ教材として使用してください。
