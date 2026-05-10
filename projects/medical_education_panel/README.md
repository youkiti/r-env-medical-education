# medical_education_panel

医学教育者向けの **準実験法 (ITS / DID)** ハンズオン用練習プロジェクト。
**カリキュラム改革という制度介入を、IR (institutional research) データの年度パネルで評価する**、という医学教育研究の典型シナリオを題材にしている。

Day 1 の `medical_education_admissions/` は **後ろ向きコホート + 重回帰** (お経表の左下) を扱った。本プロジェクトはその先で、**ランダム化できない介入を時間軸で評価する** 道具立て (ITS / DID) を扱う。

## 想定 RQ

> **2022 年度の新カリキュラム導入により、TUMS 医学生の CBSE 一発合格率と GPA はどう変化したか?**

| 要素 | 内容 |
|------|------|
| **P** | TUMS 医学部 入学コホート (2017〜2026 年度入学、各 n≈150) |
| **E** | 2022 年度入学コホートからの新カリキュラム (症例ベース学習＋臨床推論枠倍増) |
| **C** | 2022 年度より前の旧カリキュラム / 並行して未導入の他大学 (DID 用) |
| **O** | ① CBSE 一発合格率 (2値、年度集計) ② GPA (連続、年度集計) |
| Estimand | **ITS**: 介入後の水準ジャンプ + 傾き変化<br>**DID**: 介入校 × 介入後 の交互作用係数 |

## 元論文 (仮想データのモデル)

> Behnam et al. **Admission Routes and Demographics as Predictors of Academic Performance in Medical Students.** *Advances in Medical Education and Practice (AMEP)*, 2026. DOI: 10.2147/AMEP.S574930.

Day 1 と同じ TUMS の医学教育コホートを背景にしつつ、**入学経路** ではなく **カリキュラム改革** を介入として再構成。

`set.seed(20260514)` で生成された **仮想 IR パネルデータ** であり、実データではない。

### 介入の設計

```
2017 ─ 2018 ─ 2019 ─ 2020 ─ 2021 │ 2022 ─ 2023 ─ 2024 ─ 2025 ─ 2026
                                  ╳ 新カリキュラム導入
└────────  介入前 5 年  ────────┘└────────  介入後 5 年  ────────┘
```

- 介入前 5 年: TUMS と University B の `mean_gpa` は **緩く平行** (= DID の前提)
- 2022 年に TUMS の `mean_gpa` は **+0.5 水準ジャンプ** + 緩い post-trend
- `cbse_pass_rate` は +0.05 (5 percentage points) ジャンプ + 緩い post-trend
- University B には介入なし

## ディレクトリ構成

```
medical_education_panel/
├── README.md                       # このファイル
├── check_environment.R             # 事前課題：環境動作確認スクリプト
├── data/
│   ├── raw/
│   │   └── generate_panel_data.R   # 2 つの CSV を再現生成するスクリプト
│   └── processed/
│       ├── tums_panel.csv          # TUMS 単独 10 年パネル (ITS 用)
│       └── multi_school_panel.csv  # TUMS + UniB 2 校 × 10 年 (DID 用)
├── scripts/                        # 受講生の作業ファイル置き場 (空)
└── output/
    ├── figures/                    # 受講生が作る図 (空)
    └── tables/                     # 受講生が作る表 (空)
```

`analysis_panel.Rmd` は **置いていない**。WS 当日、受講生が AI と対話しながらゼロから書く (Day 1 と同じ流儀)。

## 変数辞書

### `tums_panel.csv` — ITS 用 (10 行)

| 変数 | 型 | 内容 |
|------|----|------|
| `year` | int | 入学年度 (2017〜2026) |
| `cohort_size` | int | その年度の入学コホート人数 (≈150) |
| `mean_gpa` | 連続 | 卒業時 GPA の年度平均 (20 点満点) |
| `cbse_pass_rate` | 連続 (0–1) | CBSE 一発合格率 |
| `intervention` | 2値 | 介入後 = 1 / 介入前 = 0 (2022 以降が 1) |
| `time` | int | 1 から始まる時点番号 (2017=1, ..., 2026=10) |
| `time_after_intervention` | int | 介入後 1, 2, 3, ... / 介入前 = 0 |

### `multi_school_panel.csv` — DID 用 (20 行 = 2 校 × 10 年)

| 変数 | 型 | 内容 |
|------|----|------|
| `year` | int | 入学年度 (2017〜2026) |
| `school` | カテゴリ | `TUMS` (介入校) / `UniB` (対照校) |
| `cohort_size` | int | その年度の入学コホート人数 |
| `mean_gpa` | 連続 | 卒業時 GPA の年度平均 |
| `cbse_pass_rate` | 連続 (0–1) | CBSE 一発合格率 |
| `period` | カテゴリ | `pre` (2021 以前) / `post` (2022 以降) |
| `treated` | 2値 | TUMS = 1 / UniB = 0 |

## ワークショップ課題 (受講生用)

Day 1 のフォーク済みリポジトリ上で、**空の `analysis_panel.Rmd` を新規作成** → AI と対話しながら以下の 4 ステップを埋める。

### Task 1: パネル CSV を読み込み + 折れ線プロット

- `tums_panel.csv` と `multi_school_panel.csv` を `read.csv` で読み込み
- `ggplot2` で `year` × `mean_gpa` / `cbse_pass_rate` の折れ線
- **2022 年に介入の縦線** (`geom_vline(xintercept = 2022, linetype = "dashed")`) を入れる
- `multi_school_panel` のほうは `school` で色分け (`color = school`)

### Task 2: ITS — segmented regression

`tums_panel.csv` を使って:

```r
fit_its_gpa <- lm(
  mean_gpa ~ time + intervention + time_after_intervention,
  data = tums_panel
)
gtsummary::tbl_regression(fit_its_gpa)
```

| 項 | 解釈 |
|---|---|
| `time` | 介入前のトレンド (傾き) |
| `intervention` | **水準ジャンプ** (介入直後の段差) |
| `time_after_intervention` | 介入後の **傾き変化** |

`cbse_pass_rate` でも同じことをする (2 値だが今回は **割合の年度集計** なので連続として扱う。割合データに厳密にやるなら `glm(family = binomial)` だが本コマでは深入りしない)。

### Task 3: DID — 交互作用項

`multi_school_panel.csv` を使って:

```r
multi$school <- factor(multi$school, levels = c("UniB", "TUMS"))
multi$period <- factor(multi$period, levels = c("pre",  "post"))

fit_did_gpa <- lm(
  mean_gpa ~ school + period + school:period,
  data = multi
)
gtsummary::tbl_regression(fit_did_gpa)
```

`school:period` (= `schoolTUMS:periodpost`) の係数が **DID 推定値**。
**時間経過のトレンドを除いた、TUMS 新カリキュラムの追加効果**。

### Task 4: knit して HTML レポート

- RStudio の Knit ボタン or `rmarkdown::render("analysis_panel.Rmd")`
- 出力に「ITS の水準ジャンプ・傾き変化」「DID 推定値」を要約した節を入れる
- エラーが出たら **エラーメッセージごと AI に貼って** 質問

## 期待される結果 (sanity check)

`set.seed(20260514)` で生成したデータの場合 (`Rscript data/raw/generate_panel_data.R` 末尾参照):

### ITS (TUMS, mean_gpa)

| 項 | 推定値 | 解釈 |
|---|---|---|
| `(Intercept)` | 16.41 | 2017 年の予測値 |
| `time` | −0.004 | 介入前は **ほぼフラット** |
| `intervention` | **+0.558** | **2022 年に水準ジャンプ +0.56** |
| `time_after_intervention` | +0.034 | 介入後は緩い右肩上がり |

### DID (mean_gpa)

| 項 | 推定値 | 解釈 |
|---|---|---|
| `(Intercept)` | 16.26 | UniB pre の baseline |
| `schoolTUMS` | +0.138 | 校間の固定差 (TUMS が +0.14 高い) |
| `periodpost` | +0.068 | 全体の時代固定差 |
| **`schoolTUMS:periodpost`** | **+0.572** | **DID 推定値 — TUMS の追加効果 +0.57** |

> 受講生にはこの「期待される結果」は当日まで見せない。AI の出力と一致するかを最後に答え合わせする。

## AI に聞くときの雛形

```
このリポジトリの projects/medical_education_panel/data/processed/tums_panel.csv を
読み込んで、year × mean_gpa の折れ線プロットを ggplot2 で描いてください。
2022 年の縦線を点線で重ねてください。R 初心者なので各行にコメントを付けてください。
```

```
tums_panel に対して、segmented regression of interrupted time series
(Wagner et al. 2002) を lm() で当てはめたいです。
モデル: mean_gpa ~ time + intervention + time_after_intervention
gtsummary::tbl_regression() で 95%CI と p 値を含む整形表を出してください。
```

```
multi_school_panel に対して difference-in-differences モデルを lm() で
当てはめたいです。
モデル: mean_gpa ~ school + period + school:period
school は (UniB, TUMS)、period は (pre, post) の順で factor 化してください。
gtsummary::tbl_regression() で交互作用項の係数 = DID 推定値が
読み取りやすい表にしてください。
```

```
knit したら次のエラーが出ました。直してください。
[エラーメッセージをそのまま貼る]
```

## 必要パッケージ

Day 1 と同じ。**親リポジトリの `renv.lock` にすべて含まれている**ので、
`renv::restore()` を一度通せば追加インストールは不要。

| パッケージ | 用途 |
|------------|------|
| `rmarkdown` / `knitr` | Rmd → HTML への knit |
| `gtsummary` / `broom` | 回帰表 (`tbl_regression`) |
| `dplyr` | データ操作 |
| `ggplot2` | 折れ線プロット |

> ⚠️ **AI が `nlme` `gls` `Newey-West` 等で自己相関補正を提案してきても、本コマでは深入りしない。**
> 「素の `lm()` で見せて、自己相関は限界として一言だけ触れる」が方針。

## 動作確認

```r
source("projects/medical_education_panel/check_environment.R")
```

すべて `[OK]` が出れば本編ハンズオンへ。

## ハマりどころ

| 症状 | 原因 | 対処 |
|------|------|------|
| `cannot find file 'data/processed/tums_panel.csv'` | knit 時の作業ディレクトリ | `analysis_panel.Rmd` は `projects/medical_education_panel/` 直下に置く。または `here::here(...)` を使う |
| DID で `period` のカテゴリ順が逆になり係数の符号が反転 | factor levels 未指定 | `factor(period, levels = c("pre", "post"))` を明示 |
| ITS で `time_after_intervention` が定義されていない | データ生成のみで提供 | 元 CSV にすでに列がある (再計算不要) |
| `tbl_regression` で日本語ラベル | 任意 | `label = list(intervention ~ "介入後", ...)` で変えられる |

## 「お経」表との対応 (再掲)

| アウトカム変数 | 2値 | 連続 | **時系列パネル** |
|----------------|-----|------|------------------|
| 分布の記述 | 頻度集計 | 平均 (SD) | **折れ線プロット (年度 × アウトカム)** |
| 単変量解析 | $\chi^2$ | t 検定 | — |
| 多変量解析 | ロジ回帰 | 重回帰 | **ITS (`lm + segmented`)** / **DID (`lm + 交互作用`)** |

Day 1 のお経表に **「時系列パネル」列** が増えたイメージ。中身は結局 `lm()` の応用。

## データを再生成する場合

```r
source("projects/medical_education_panel/data/raw/generate_panel_data.R")
# data/processed/tums_panel.csv, multi_school_panel.csv が上書きされる
```

`set.seed(20260514)` 固定なので、何度実行しても同じ CSV が得られる。
