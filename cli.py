#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お腹がすいた開発猫の物語 - CLI Tool
コマンドライン インターフェース
"""

import argparse
import sys
from pathlib import Path
from story_manager import StoryManager
from distribution_system import DistributionSystem


def create_story_command(args):
    """新しい物語を作成"""
    manager = StoryManager()
    
    if args.interactive:
        # インタラクティブモード
        print("=== 新しいエピソード作成 ===")
        episode_num = int(input("エピソード番号: "))
        title = input("タイトル: ")
        print("内容を入力してください（空行で終了）:")
        
        content_lines = []
        while True:
            line = input()
            if line == "":
                break
            content_lines.append(line)
        content = "\n".join(content_lines)
        
        keywords = input("技術キーワード（カンマ区切り）: ").split(",")
        keywords = [k.strip() for k in keywords if k.strip()]
        
    else:
        episode_num = args.episode
        title = args.title
        content = args.content
        keywords = args.keywords or []
    
    story = manager.create_story(episode_num, title, content, keywords)
    print(f"✅ エピソード {story['episode']} を作成しました: {story['title']}")
    print(f"📝 文字数: {story['word_count']}")
    print(f"🏷️  猫語化用語: {len(story['cat_terms_used'])}個")


def list_stories_command(args):
    """物語一覧を表示"""
    manager = StoryManager()
    stories = manager.list_stories()
    
    if not stories:
        print("📚 まだエピソードがありません")
        return
    
    print("=== お腹がすいた開発猫の物語 エピソード一覧 ===")
    for story in stories:
        status_icon = {"draft": "📝", "scheduled": "⏰", "published": "✅"}.get(story["status"], "❓")
        print(f"{status_icon} 第{story['episode']:02d}話: {story['title']}")
        print(f"   文字数: {story['word_count']} | ステータス: {story['status']}")
        if story.get("tech_keywords"):
            print(f"   キーワード: {', '.join(story['tech_keywords'])}")
        print()


def publish_command(args):
    """エピソードを配信"""
    dist_system = DistributionSystem()
    
    platforms = args.platforms or ["qiita", "zenn", "twitter"]
    
    print(f"🚀 エピソード {args.episode} を配信中...")
    results = dist_system.publish_episode(args.episode, platforms)
    
    print(f"📅 配信完了: {results['published_at']}")
    for platform, result in results["results"].items():
        status = "✅" if result["success"] else "❌"
        message = result.get("url", result.get("message", ""))
        print(f"{platform}: {status} {message}")


def schedule_command(args):
    """配信スケジュールを設定"""
    dist_system = DistributionSystem()
    
    schedule_data = dist_system.schedule_publication(args.episode, args.date)
    
    print(f"⏰ エピソード {args.episode} の配信をスケジュールしました")
    print(f"📅 配信予定日: {schedule_data['scheduled_date']} {schedule_data['scheduled_time']}")


def status_command(args):
    """全体ステータスを表示"""
    manager = StoryManager()
    dist_system = DistributionSystem()
    
    schedule = manager.get_publishing_schedule()
    analytics = dist_system.get_analytics_summary()
    
    print("=== お腹がすいた開発猫の物語 ステータス ===")
    print()
    print("📊 エピソード統計:")
    print(f"   総エピソード: {analytics['total_episodes']}")
    print(f"   公開済み: {analytics['published_episodes']}")
    print(f"   ドラフト: {schedule['draft']}")
    print(f"   スケジュール済み: {schedule['scheduled']}")
    print()
    print("📝 コンテンツ統計:")
    print(f"   総文字数: {analytics['total_words']:,}")
    print(f"   平均文字数: {analytics['average_words_per_episode']:.0f}")
    print()
    print("📅 スケジュール:")
    print(f"   次回配信予定: {schedule['next_publication'][:10]}")
    print()
    print("🚀 プラットフォーム:")
    for platform, config in analytics['platforms_summary'].items():
        status = "✅" if config['enabled'] else "❌"
        print(f"   {platform}: {status}")


def export_command(args):
    """プラットフォーム別にエクスポート"""
    manager = StoryManager()
    
    content = manager.export_for_platform(args.episode, args.platform)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 {args.platform}形式でエクスポート完了: {args.output}")
    else:
        print(f"=== エピソード {args.episode} - {args.platform}形式 ===")
        print(content)


def report_command(args):
    """月次レポートを生成"""
    dist_system = DistributionSystem()
    
    report = dist_system.create_monthly_report()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📈 月次レポートを生成しました: {args.output}")
    else:
        print(report)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="お腹がすいた開発猫の物語 - 配信システム CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 新しいエピソードを作成
  python cli.py create --episode 2 --title "バグとマグロ" --content "今日は..." --keywords "Python,バグ修正"
  
  # インタラクティブモードで作成
  python cli.py create --interactive
  
  # エピソード一覧を表示
  python cli.py list
  
  # エピソードを配信
  python cli.py publish --episode 1
  
  # 特定のプラットフォームのみに配信
  python cli.py publish --episode 1 --platforms qiita zenn
  
  # 配信スケジュールを設定
  python cli.py schedule --episode 2 --date 2025-07-01
  
  # 全体ステータスを確認
  python cli.py status
  
  # プラットフォーム別にエクスポート
  python cli.py export --episode 1 --platform qiita --output episode1_qiita.md
  
  # 月次レポート生成
  python cli.py report --output monthly_report.md
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="使用可能なコマンド")
    
    # create サブコマンド
    create_parser = subparsers.add_parser("create", help="新しいエピソードを作成")
    create_parser.add_argument("--episode", type=int, help="エピソード番号")
    create_parser.add_argument("--title", help="タイトル")
    create_parser.add_argument("--content", help="内容")
    create_parser.add_argument("--keywords", nargs="*", help="技術キーワード")
    create_parser.add_argument("--interactive", action="store_true", help="インタラクティブモード")
    
    # list サブコマンド
    list_parser = subparsers.add_parser("list", help="エピソード一覧を表示")
    
    # publish サブコマンド
    publish_parser = subparsers.add_parser("publish", help="エピソードを配信")
    publish_parser.add_argument("--episode", type=int, required=True, help="エピソード番号")
    publish_parser.add_argument("--platforms", nargs="*", choices=["qiita", "zenn", "twitter"], help="配信プラットフォーム")
    
    # schedule サブコマンド
    schedule_parser = subparsers.add_parser("schedule", help="配信スケジュールを設定")
    schedule_parser.add_argument("--episode", type=int, required=True, help="エピソード番号")
    schedule_parser.add_argument("--date", help="配信予定日 (YYYY-MM-DD)")
    
    # status サブコマンド
    status_parser = subparsers.add_parser("status", help="全体ステータスを表示")
    
    # export サブコマンド
    export_parser = subparsers.add_parser("export", help="プラットフォーム別にエクスポート")
    export_parser.add_argument("--episode", type=int, required=True, help="エピソード番号")
    export_parser.add_argument("--platform", choices=["qiita", "zenn", "sns"], required=True, help="プラットフォーム")
    export_parser.add_argument("--output", help="出力ファイル名")
    
    # report サブコマンド
    report_parser = subparsers.add_parser("report", help="月次レポートを生成")
    report_parser.add_argument("--output", help="出力ファイル名")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "create":
            create_story_command(args)
        elif args.command == "list":
            list_stories_command(args)
        elif args.command == "publish":
            publish_command(args)
        elif args.command == "schedule":
            schedule_command(args)
        elif args.command == "status":
            status_command(args)
        elif args.command == "export":
            export_command(args)
        elif args.command == "report":
            report_command(args)
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()