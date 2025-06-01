#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お腹がすいた開発猫の物語 - Distribution System
各プラットフォームへの配信自動化システム
"""

import json
import requests
import datetime
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from story_manager import StoryManager


class DistributionSystem:
    """配信システムクラス"""
    
    def __init__(self, config_file: str = "distribution_config.yaml"):
        self.config_file = Path(config_file)
        self.story_manager = StoryManager()
        self.load_config()
        
    def load_config(self):
        """設定ファイルを読み込み"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            # デフォルト設定を作成
            self.config = {
                "platforms": {
                    "qiita": {
                        "enabled": True,
                        "api_token": "YOUR_QIITA_TOKEN",
                        "organization": "",
                        "auto_publish": False
                    },
                    "zenn": {
                        "enabled": True,
                        "username": "YOUR_ZENN_USERNAME",
                        "auto_publish": False
                    },
                    "twitter": {
                        "enabled": True,
                        "api_key": "YOUR_TWITTER_API_KEY",
                        "api_secret": "YOUR_TWITTER_API_SECRET",
                        "access_token": "YOUR_ACCESS_TOKEN",
                        "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET"
                    }
                },
                "schedule": {
                    "publication_day": 1,  # 月初
                    "publication_time": "09:00",
                    "timezone": "Asia/Tokyo"
                },
                "analytics": {
                    "target_views_per_episode": 1000,
                    "target_shares_per_episode": 100
                }
            }
            self.save_config()
    
    def save_config(self):
        """設定ファイルを保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def publish_to_qiita(self, episode_number: int) -> Dict:
        """Qiitaに記事を投稿"""
        if not self.config["platforms"]["qiita"]["enabled"]:
            return {"success": False, "message": "Qiita publication disabled"}
        
        story = self.story_manager.get_story(episode_number)
        if not story:
            return {"success": False, "message": f"Episode {episode_number} not found"}
        
        content = self.story_manager.export_for_platform(episode_number, "qiita")
        
        # Qiita API用のデータ準備
        article_data = {
            "title": story["title"],
            "body": content,
            "tags": [
                {"name": "プログラミング"},
                {"name": "開発"},
                {"name": "猫"},
                {"name": "エッセイ"}
            ] + [{"name": kw} for kw in story.get("tech_keywords", [])[:6]],  # 最大10タグ
            "private": not self.config["platforms"]["qiita"]["auto_publish"],
            "tweet": True
        }
        
        # NOTE: 実際のAPI呼び出しはここに実装
        # headers = {"Authorization": f"Bearer {self.config['platforms']['qiita']['api_token']}"}
        # response = requests.post("https://qiita.com/api/v2/items", json=article_data, headers=headers)
        
        # シミュレーション
        print(f"[SIMULATION] Publishing to Qiita: {story['title']}")
        return {
            "success": True,
            "platform": "qiita",
            "url": f"https://qiita.com/simulation/items/{episode_number}",
            "published_at": datetime.datetime.now().isoformat()
        }
    
    def publish_to_zenn(self, episode_number: int) -> Dict:
        """Zennに記事を投稿（GitHub連携）"""
        if not self.config["platforms"]["zenn"]["enabled"]:
            return {"success": False, "message": "Zenn publication disabled"}
        
        story = self.story_manager.get_story(episode_number)
        if not story:
            return {"success": False, "message": f"Episode {episode_number} not found"}
        
        content = self.story_manager.export_for_platform(episode_number, "zenn")
        
        # Zenn用のマークダウンファイルを生成
        zenn_dir = Path("zenn_articles")
        zenn_dir.mkdir(exist_ok=True)
        
        filename = f"hungry-cat-episode-{episode_number:02d}.md"
        zenn_file = zenn_dir / filename
        
        with open(zenn_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[SIMULATION] Zenn article generated: {zenn_file}")
        return {
            "success": True,
            "platform": "zenn",
            "filename": filename,
            "url": f"https://zenn.dev/{self.config['platforms']['zenn']['username']}/articles/{filename.replace('.md', '')}",
            "published_at": datetime.datetime.now().isoformat()
        }
    
    def publish_to_twitter(self, episode_number: int) -> Dict:
        """Twitterに投稿"""
        if not self.config["platforms"]["twitter"]["enabled"]:
            return {"success": False, "message": "Twitter publication disabled"}
        
        story = self.story_manager.get_story(episode_number)
        if not story:
            return {"success": False, "message": f"Episode {episode_number} not found"}
        
        content = self.story_manager.export_for_platform(episode_number, "sns")
        
        # Twitter文字数制限チェック
        if len(content) > 280:
            content = content[:277] + "..."
        
        # NOTE: 実際のTwitter API呼び出しはここに実装
        # twitter_api = TwitterAPI(...)
        # response = twitter_api.post_tweet(content)
        
        print(f"[SIMULATION] Publishing to Twitter: {content[:50]}...")
        return {
            "success": True,
            "platform": "twitter",
            "tweet_id": f"simulation_{episode_number}",
            "url": f"https://twitter.com/simulation/status/{episode_number}",
            "published_at": datetime.datetime.now().isoformat()
        }
    
    def publish_episode(self, episode_number: int, platforms: List[str] = None) -> Dict:
        """指定されたエピソードを各プラットフォームに配信"""
        if platforms is None:
            platforms = ["qiita", "zenn", "twitter"]
        
        results = {
            "episode": episode_number,
            "published_at": datetime.datetime.now().isoformat(),
            "results": {}
        }
        
        for platform in platforms:
            if platform == "qiita":
                results["results"]["qiita"] = self.publish_to_qiita(episode_number)
            elif platform == "zenn":
                results["results"]["zenn"] = self.publish_to_zenn(episode_number)
            elif platform == "twitter":
                results["results"]["twitter"] = self.publish_to_twitter(episode_number)
        
        # 配信結果を記録
        self._save_publication_log(results)
        
        # ストーリーのステータスを更新
        self.story_manager.update_story_status(episode_number, "published")
        
        return results
    
    def _save_publication_log(self, results: Dict):
        """配信ログを保存"""
        log_dir = Path("publication_logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"episode_{results['episode']:02d}_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def schedule_publication(self, episode_number: int, target_date: str = None):
        """公開スケジュールを設定"""
        if target_date is None:
            # 次の月初を計算
            now = datetime.datetime.now()
            next_month = now.replace(day=1) + datetime.timedelta(days=32)
            target_date = next_month.replace(day=1).strftime("%Y-%m-%d")
        
        schedule_data = {
            "episode": episode_number,
            "scheduled_date": target_date,
            "scheduled_time": self.config["schedule"]["publication_time"],
            "platforms": ["qiita", "zenn", "twitter"],
            "status": "scheduled"
        }
        
        schedule_dir = Path("publication_schedule")
        schedule_dir.mkdir(exist_ok=True)
        
        schedule_file = schedule_dir / f"episode_{episode_number:02d}_schedule.json"
        with open(schedule_file, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=2)
        
        # ストーリーのステータスを更新
        self.story_manager.update_story_status(episode_number, "scheduled")
        
        return schedule_data
    
    def get_analytics_summary(self) -> Dict:
        """配信分析サマリーを取得"""
        stories = self.story_manager.list_stories()
        published_stories = [s for s in stories if s["status"] == "published"]
        
        analytics = {
            "total_episodes": len(stories),
            "published_episodes": len(published_stories),
            "total_words": sum(s["word_count"] for s in stories),
            "average_words_per_episode": sum(s["word_count"] for s in stories) / len(stories) if stories else 0,
            "publication_rate": len(published_stories) / len(stories) if stories else 0,
            "platforms_summary": {
                "qiita": {"enabled": self.config["platforms"]["qiita"]["enabled"]},
                "zenn": {"enabled": self.config["platforms"]["zenn"]["enabled"]},
                "twitter": {"enabled": self.config["platforms"]["twitter"]["enabled"]}
            }
        }
        
        return analytics
    
    def create_monthly_report(self) -> str:
        """月次レポートを生成"""
        analytics = self.get_analytics_summary()
        schedule = self.story_manager.get_publishing_schedule()
        
        report = f"""
# お腹がすいた開発猫の物語 - 月次レポート

## 📊 配信統計
- 総エピソード数: {analytics['total_episodes']}
- 公開済み: {analytics['published_episodes']}
- 総文字数: {analytics['total_words']:,}文字
- エピソード平均文字数: {analytics['average_words_per_episode']:.0f}文字

## 📅 公開スケジュール
- 次回公開予定: {schedule['next_publication'][:10]}
- ドラフト: {schedule['draft']}話
- スケジュール済み: {schedule['scheduled']}話

## 🚀 プラットフォーム状況
- Qiita: {'✅' if analytics['platforms_summary']['qiita']['enabled'] else '❌'}
- Zenn: {'✅' if analytics['platforms_summary']['zenn']['enabled'] else '❌'}
- Twitter: {'✅' if analytics['platforms_summary']['twitter']['enabled'] else '❌'}

## 🎯 次のアクション
1. 新しいエピソードの執筆
2. SNSでのプロモーション
3. 読者フィードバックの確認

---
Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return report.strip()


def main():
    """メイン関数 - サンプル使用例"""
    dist_system = DistributionSystem()
    
    print("=== お腹がすいた開発猫の物語 配信システム ===\n")
    
    # 設定確認
    print("📋 Current configuration:")
    print(f"Qiita enabled: {dist_system.config['platforms']['qiita']['enabled']}")
    print(f"Zenn enabled: {dist_system.config['platforms']['zenn']['enabled']}")
    print(f"Twitter enabled: {dist_system.config['platforms']['twitter']['enabled']}")
    print()
    
    # エピソード1を配信（シミュレーション）
    print("🚀 Publishing episode 1...")
    results = dist_system.publish_episode(1)
    print(f"Publication completed at: {results['published_at']}")
    
    for platform, result in results["results"].items():
        status = "✅" if result["success"] else "❌"
        print(f"{platform}: {status} {result.get('url', result.get('message', ''))}")
    print()
    
    # 分析サマリー表示
    analytics = dist_system.get_analytics_summary()
    print("📊 Analytics summary:")
    print(f"Total episodes: {analytics['total_episodes']}")
    print(f"Published: {analytics['published_episodes']}")
    print(f"Average words: {analytics['average_words_per_episode']:.0f}")
    print()
    
    # 月次レポート生成
    report = dist_system.create_monthly_report()
    print("📈 Monthly report:")
    print(report)


if __name__ == "__main__":
    main()