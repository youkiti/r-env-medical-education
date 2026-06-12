# R環境のトラブルシューティングガイド

このドキュメントでは、R環境や統計解析パッケージに関する一般的な問題と解決策を提供します。

## パッケージのインストール問題

### 権限エラー

```
Warning: 'lib = "/usr/local/lib/R/site-library"' is not writable
```

**解決策**:
- ユーザー専用ライブラリにインストールする（Windows / Mac どちらでも動作）
  ```r
  install.packages("パッケージ名", lib = Sys.getenv("R_LIBS_USER"))
  ```
  `Sys.getenv("R_LIBS_USER")` は OS ごとに適切なパスを返します（Windows: `AppData/Local/R/win-library/…`、Mac: `~/Library/R/…`）。空のときは以下で確認・作成できます:
  ```r
  path <- Sys.getenv("R_LIBS_USER")
  if (!dir.exists(path)) dir.create(path, recursive = TRUE)
  ```

### 依存関係の問題

```
ERROR: dependencies 'パッケージ名' are not available for package
```

**解決策**:
- 依存パッケージを先にインストールする
- `dependencies = TRUE` オプションを使用する
  ```r
  install.packages("パッケージ名", dependencies = TRUE)
  ```

### リポジトリの問題

```
Warning: unable to access index for repository
```

**解決策**:
- 別のCRANミラーを試す
  ```r
  install.packages("パッケージ名", repos = "https://cran.rstudio.com/")
  ```

## パッケージの読み込み問題

### バージョンの不一致

```
Error: package or namespace load failed for 'パッケージ名'
```

**解決策**:
- パッケージを再インストールする
  ```r
  remove.packages("パッケージ名")
  install.packages("パッケージ名")
  ```
- Rのバージョンを確認する
  ```r
  R.version.string
  ```

### 名前空間の衝突

```
The following object is masked from 'package:パッケージ名'
```

**解決策**:
- 特定のパッケージから関数を明示的に呼び出す
  ```r
  パッケージ名::関数名()
  ```
- パッケージの読み込み順序を変更する

## データ操作の問題

### tidyverseでの一般的なエラー

```
Error: Can't subset columns that don't exist.
```

**解決策**:
- 列名のスペルを確認する
- データフレームの構造を確認する
  ```r
  str(データフレーム)
  names(データフレーム)
  ```

### 因子型の問題

```
Warning: Unknown or uninitialised column: 'カラム名'.
```

**解決策**:
- 因子レベルを確認・修正する
  ```r
  levels(データフレーム$カラム名)
  データフレーム$カラム名 <- factor(データフレーム$カラム名, levels = c("レベル1", "レベル2"))
  ```

## 統計モデルの問題

### 収束エラー

```
Warning: glm.fit: algorithm did not converge
```

**解決策**:
- 説明変数間の多重共線性を確認する
- サンプルサイズを確認する
- モデルを単純化する
- 変数のスケーリングを行う

### 傾向スコア解析の問題

```
Error in weightit: propensity scores close to 0 or 1
```

**解決策**:
- 極端な傾向スコアを持つ観測値を確認する
- トリミングを適用する
  ```r
  w_out <- weightit(treatment ~ covariates, data = data, method = "ps", trim = 0.01)
  ```
- 異なる推定方法を試す
  ```r
  w_out <- weightit(treatment ~ covariates, data = data, method = "gbm")
  ```

## グラフ作成の問題

### ggplot2のエラー

```
Error: Aesthetics must be either length 1 or the same as the data
```

**解決策**:
- データの構造を確認する
- 長形式データに変換する
  ```r
  データ_長形式 <- pivot_longer(データ, cols = c("列1", "列2"), names_to = "変数", values_to = "値")
  ```

### 保存の問題

```
Error in dev.off() : cannot shut down device 1 (the null device)
```

**解決策**:
- グラフを保存する前にプロットを作成する
- 正しいディレクトリパスを指定する
  ```r
  ggsave("ファイル名.png", plot = プロット, path = "パス")
  ```

## パフォーマンスの問題

### メモリ不足

```
Error: cannot allocate vector of size X Mb
```

**解決策**:
- データの一部だけを使用する
- 不要なオブジェクトを削除する
  ```r
  rm(list = ls())
  gc()
  ```
- データ.tableやarrowなどの効率的なパッケージを使用する

### 処理速度の問題

**解決策**:
- apply系関数やpurrrを使用する
- データ.tableを使用する
- 並列処理を検討する
  ```r
  library(parallel)
  library(foreach)
  library(doParallel)
  ```

## その他の役立つヒント

- セッション情報を確認する
  ```r
  sessionInfo()
  ```
- エラーメッセージを検索する
  - [Stack Overflow](https://stackoverflow.com/questions/tagged/r)
  - [RStudio Community](https://community.rstudio.com/)
- Rのバージョンとパッケージの互換性を確認する
- 定期的にパッケージを更新する
  ```r
  update.packages()
  ```
