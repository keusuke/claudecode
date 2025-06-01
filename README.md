# お腹がすいた開発猫の物語 - 配信システム

開発者の日常を猫の視点から描く物語シリーズの配信管理システム

## 概要

「お腹がすいた開発猫の物語」は、茶トラ猫のデバッグ（通称：デバ）が主人公の開発者向けストーリーシリーズです。
このリポジトリは、物語の作成・管理・配信を自動化するシステムを提供します。

### 主なキャラクター
- **デバッグ (デバ)**: 茶トラ猫、3歳、食いしん坊で好奇心旺盛
- **田中さん**: エンジニア、28歳、デバの飼い主
- **コンパイル**: 白猫、几帳面な性格
- **ギット**: 黒猫、クールな性格

## 機能

### 🐱 物語管理 (`story_manager.py`)
- エピソードの作成・編集・管理
- キャラクター設定とプログラミング用語の猫語化
- 物語のステータス管理（ドラフト・スケジュール済み・公開済み）

### 🚀 配信システム (`distribution_system.py`)
- 複数プラットフォームへの自動配信
  - Qiita
  - Zenn
  - Twitter/SNS
- プラットフォーム別フォーマット変換
- 配信スケジュール管理

### 💻 CLI ツール (`cli.py`)
直感的なコマンドライン操作で全機能にアクセス

## インストール

```bash
# 依存関係をインストール
pip install -r requirements.txt

# 基本的な使用例
python cli.py status
```

## 使用方法

### 基本コマンド

```bash
# エピソード一覧表示
python cli.py list

# 新しいエピソード作成（インタラクティブ）
python cli.py create --interactive

# エピソード作成（コマンドライン）
python cli.py create --episode 2 --title "バグとマグロ" --content "今日は..." --keywords "Python,デバッグ"

# エピソード配信
python cli.py publish --episode 1

# 特定プラットフォームのみ配信
python cli.py publish --episode 1 --platforms qiita zenn

# 配信スケジュール設定
python cli.py schedule --episode 2 --date 2025-07-01

# プラットフォーム別エクスポート
python cli.py export --episode 1 --platform qiita --output episode1_qiita.md

# 月次レポート生成
python cli.py report --output monthly_report.md

# 全体ステータス確認
python cli.py status
```

### 設定ファイル

`distribution_config.yaml` で各プラットフォームの設定を管理：

```yaml
platforms:
  qiita:
    enabled: true
    api_token: "YOUR_QIITA_TOKEN"
    auto_publish: false
  zenn:
    enabled: true
    username: "YOUR_ZENN_USERNAME"
  twitter:
    enabled: true
    api_key: "YOUR_TWITTER_API_KEY"
    # ... その他の設定
```

## ディレクトリ構造

```
├── story_manager.py          # 物語管理システム
├── distribution_system.py    # 配信システム
├── cli.py                    # コマンドラインインターフェース
├── distribution_config.yaml  # 配信設定
├── requirements.txt          # Python依存関係
├── stories/                  # エピソードファイル
│   └── episode_01.json
├── zenn_articles/           # Zenn用記事（自動生成）
├── publication_logs/        # 配信ログ
└── publication_schedule/    # 配信スケジュール
```

## プログラミング用語の猫語化

システムには開発用語を猫らしい表現に変換する機能があります：

- コミット → ニャミット
- デバッグ → 毛づくろい
- エラー → 毛玉
- バグ → 虫
- テスト → 匂い確認
- デプロイ → お外に出る

## 配信スケジュール

- **頻度**: 月刊（月初公開）
- **文字数**: 2000〜3000文字/話
- **ターゲット**: ソフトウェア開発者、プログラミング学習者、猫好きな技術者

## 成功指標

- 各話1,000PV以上
- SNSシェア100件以上/話
- ハッシュタグ `#お腹すいた開発猫` での拡散

## 今後の展開

- グッズ化（ステッカー、LINEスタンプ）
- 書籍化
- 開発者イベントでのコラボレーション

## claude code の練習用リポジトリ

このプロジェクトは Claude Code の実践的な活用例としても機能します。
