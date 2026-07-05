---
name: delegate-to-codex
description: Launches OpenAI Codex CLI with context from the current host-agent session to delegate coding tasks.
---

# Delegate to Codex

## Scope

- Utility skill for assisted ideation or debugging.
- Not part of the 16-skill core clinical epidemiology workflow.

Codex CLI をアイデア生成・デバッグ支援として活用。Codex がコード/解決策を提案し、ホストエージェント（Antigravity / Claude Code / Gemini 等）がファイル操作を実行。

## 使い方

ワークフロー `/codex [task]` を使用:
- `/codex このエラーを修正して: [error message]`
- `/codex この関数をリファクタリングして`
- `/codex テストを追加して`

## 役割分担

| 役割 | 担当 |
|-----|-----|
| コード生成・提案 | Codex |
| ファイル作成・編集 | ホストエージェント |
| コマンド実行・検証 | ホストエージェント |

## 内部動作

1. ホストエージェントが `codex exec` でタスクを送信
2. Codex が解決策・コードを出力
3. ホストエージェントが出力をパースしてファイル操作
4. ホストエージェントが検証・結果報告

