#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お腹がすいた開発猫の物語 - Story Management System
配信システムのメインモジュール
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class StoryManager:
    """物語管理クラス"""
    
    def __init__(self, stories_dir: str = "stories"):
        self.stories_dir = Path(stories_dir)
        self.stories_dir.mkdir(exist_ok=True)
        
        # キャラクター設定
        self.characters = {
            "debug": {
                "name": "デバッグ",
                "nickname": "デバ",
                "species": "茶トラ猫",
                "age": 3,
                "personality": "好奇心旺盛だが食いしん坊",
                "catchphrases": ["お腹すいた〜", "ニャーコード書けない"]
            },
            "compile": {
                "name": "コンパイル",
                "species": "白猫",
                "personality": "几帳面"
            },
            "git": {
                "name": "ギット", 
                "species": "黒猫",
                "personality": "クール"
            },
            "tanaka": {
                "name": "田中さん",
                "role": "エンジニア",
                "age": 28,
                "relationship": "デバッグの飼い主"
            }
        }
        
        # プログラミング用語の猫語化辞書
        self.cat_terms = {
            "コミット": "ニャミット",
            "デバッグ": "毛づくろい",
            "エラー": "毛玉",
            "バグ": "虫",
            "テスト": "匂い確認",
            "デプロイ": "お外に出る",
            "マージ": "仲良くする",
            "リファクタリング": "毛繕い直し"
        }

    def create_story(self, episode_number: int, title: str, content: str, 
                    tech_keywords: List[str] = None) -> Dict:
        """新しい物語エピソードを作成"""
        story_data = {
            "episode": episode_number,
            "title": title,
            "content": content,
            "tech_keywords": tech_keywords or [],
            "characters_featured": ["debug"],  # デフォルトは主人公
            "cat_terms_used": [],
            "created_date": datetime.datetime.now().isoformat(),
            "status": "draft",
            "word_count": len(content),
            "target_platforms": ["qiita", "zenn", "sns"]
        }
        
        # 猫語化された用語を検出
        for original, cat_term in self.cat_terms.items():
            if cat_term in content:
                story_data["cat_terms_used"].append({
                    "original": original,
                    "cat_term": cat_term
                })
        
        # ファイルに保存
        story_file = self.stories_dir / f"episode_{episode_number:02d}.json"
        with open(story_file, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, ensure_ascii=False, indent=2)
        
        return story_data

    def get_story(self, episode_number: int) -> Optional[Dict]:
        """指定されたエピソードを取得"""
        story_file = self.stories_dir / f"episode_{episode_number:02d}.json"
        if story_file.exists():
            with open(story_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def list_stories(self) -> List[Dict]:
        """全エピソードのリストを取得"""
        stories = []
        for story_file in sorted(self.stories_dir.glob("episode_*.json")):
            with open(story_file, 'r', encoding='utf-8') as f:
                stories.append(json.load(f))
        return stories

    def update_story_status(self, episode_number: int, status: str):
        """物語のステータスを更新"""
        story = self.get_story(episode_number)
        if story:
            story["status"] = status
            story["updated_date"] = datetime.datetime.now().isoformat()
            
            story_file = self.stories_dir / f"episode_{episode_number:02d}.json"
            with open(story_file, 'w', encoding='utf-8') as f:
                json.dump(story, f, ensure_ascii=False, indent=2)

    def get_publishing_schedule(self) -> Dict:
        """公開スケジュールを生成"""
        stories = self.list_stories()
        schedule = {
            "total_episodes": len(stories),
            "published": len([s for s in stories if s["status"] == "published"]),
            "draft": len([s for s in stories if s["status"] == "draft"]),
            "scheduled": len([s for s in stories if s["status"] == "scheduled"]),
            "next_publication": None
        }
        
        # 次回公開予定を計算（月刊なので月初）
        next_month = datetime.datetime.now().replace(day=1) + datetime.timedelta(days=32)
        next_month = next_month.replace(day=1)
        schedule["next_publication"] = next_month.isoformat()
        
        return schedule

    def generate_social_hashtags(self, episode_number: int) -> List[str]:
        """SNS用ハッシュタグを生成"""
        base_tags = ["#お腹すいた開発猫", "#プログラミング", "#開発者あるある", "#猫"]
        
        story = self.get_story(episode_number)
        if story and story.get("tech_keywords"):
            for keyword in story["tech_keywords"]:
                base_tags.append(f"#{keyword}")
        
        return base_tags

    def export_for_platform(self, episode_number: int, platform: str) -> str:
        """プラットフォーム別にフォーマットして出力"""
        story = self.get_story(episode_number)
        if not story:
            return ""
        
        if platform == "qiita":
            return self._format_for_qiita(story)
        elif platform == "zenn":
            return self._format_for_zenn(story)
        elif platform == "sns":
            return self._format_for_sns(story)
        else:
            return story["content"]

    def _format_for_qiita(self, story: Dict) -> str:
        """Qiita形式でフォーマット"""
        hashtags = " ".join([f"#{kw}" for kw in story.get("tech_keywords", [])])
        
        return f"""# {story['title']}

{hashtags}

{story['content']}

---
この物語は「お腹がすいた開発猫の物語」シリーズの第{story['episode']}話です。
"""

    def _format_for_zenn(self, story: Dict) -> str:
        """Zenn形式でフォーマット"""
        frontmatter = f"""---
title: "{story['title']}"
emoji: "🐱"
type: "idea"
topics: {json.dumps(story.get('tech_keywords', []), ensure_ascii=False)}
published: true
---

"""
        return frontmatter + story['content']

    def _format_for_sns(self, story: Dict) -> str:
        """SNS形式でフォーマット（短縮版）"""
        hashtags = " ".join(self.generate_social_hashtags(story['episode']))
        
        # 内容を140文字程度に短縮
        content_preview = story['content'][:100] + "..." if len(story['content']) > 100 else story['content']
        
        return f"""{story['title']}

{content_preview}

{hashtags}
"""


def main():
    """メイン関数 - サンプル使用例"""
    manager = StoryManager()
    
    # サンプルエピソードを作成
    sample_content = """
今日もお腹がすいた。デバッグという名前の茶トラ猫、それが僕だ。

田中さんがパソコンに向かってカタカタとキーボードを叩いている。
「あ、またエラーが出た...」
そんな時こそ、僕の出番だ。

画面を見ると、赤い文字がたくさん表示されている。これは毛玉だ。
僕は田中さんのキーボードの上に座って、パニャパニャと肉球でキーを押してみる。

「おっ、ログが消えた！デバ、君はやっぱり天才プログラマーだね」

えへん。褒められると嬉しいニャ。
でも、お腹がすいた。ニャーコード書いてたらお腹が鳴っちゃった。

「はいはい、ごはんだね」

やったニャ！今日もデバッグ（毛づくろい）作業完了だニャ〜
    """
    
    story = manager.create_story(
        episode_number=1,
        title="Hello, Hungry World! - オフィス初日",
        content=sample_content.strip(),
        tech_keywords=["Python", "デバッグ", "エラー処理"]
    )
    
    print("Sample episode created:")
    print(f"Episode {story['episode']}: {story['title']}")
    print(f"Word count: {story['word_count']}")
    print(f"Cat terms used: {len(story['cat_terms_used'])}")
    
    # スケジュール表示
    schedule = manager.get_publishing_schedule()
    print(f"\nPublishing schedule:")
    print(f"Total episodes: {schedule['total_episodes']}")
    print(f"Next publication: {schedule['next_publication']}")
    
    # SNS用ハッシュタグ生成
    hashtags = manager.generate_social_hashtags(1)
    print(f"\nSNS hashtags: {' '.join(hashtags)}")


if __name__ == "__main__":
    main()