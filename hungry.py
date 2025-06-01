#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お腹がすいた開発猫の物語 - インタラクティブストーリー実装
Story of a Hungry Development Cat - Interactive Story Implementation
"""

import random
import time

class HungryCat:
    """お腹がすいた開発猫のデバッグ"""
    
    def __init__(self, name="デバッグ"):
        self.name = name
        self.hunger_level = 8  # 0-10 (10が最高にお腹すいた)
        self.energy_level = 5  # 0-10 (10が最高に元気)
        self.bugs_found = 0
        self.episodes_completed = 0
    
    def say_hungry(self):
        """お腹すいたメッセージ"""
        messages = [
            "お腹すいた〜",
            "ニャーコード書けない...",
            "おやつタイムはまだかニャ？",
            "バグよりマグロが食べたいニャン",
            "コンパイルエラーよりお腹エラーの方が深刻ニャ"
        ]
        return random.choice(messages)
    
    def find_bug(self):
        """バグを発見する"""
        if self.hunger_level > 3:  # お腹がすいていると集中力が下がる
            success_rate = 0.7
        else:
            success_rate = 0.3
        
        if random.random() < success_rate:
            self.bugs_found += 1
            self.hunger_level = min(10, self.hunger_level + 1)
            return True
        return False
    
    def eat_treat(self, treat_type="デバッグクッキー"):
        """おやつを食べる"""
        self.hunger_level = max(0, self.hunger_level - 3)
        self.energy_level = min(10, self.energy_level + 2)
        return f"{treat_type}を食べたニャン！満足度アップ！"
    
    def debug_session(self):
        """デバッグセッション"""
        print(f"\n=== {self.name}のデバッグタイム ===")
        print(self.say_hungry())
        print(f"お腹レベル: {self.hunger_level}/10")
        print(f"エネルギー: {self.energy_level}/10")
        
        if self.find_bug():
            print("🐛 バグを発見したニャン！")
            print("田中さんが喜んでくれるニャ〜")
            if self.hunger_level >= 7:
                print(self.eat_treat())
        else:
            print("今回はバグが見つからなかったニャ...")
            print(self.say_hungry())

def print_episode_intro():
    """エピソード紹介"""
    print("=" * 50)
    print("🐱 お腹がすいた開発猫の物語 🐱")
    print("第1話「Hello, Hungry World!」")
    print("=" * 50)
    print()
    
    story_intro = """
茶トラ猫のデバッグ（通称デバ）は、今日からスタートアップ企業
「ニャンコードテック」で働くことになりました。

プログラミングの知識はまだまだですが、持ち前の好奇心と
「お腹すいた」パワーで、開発チームを支えていきます！
    """
    
    for char in story_intro:
        print(char, end='', flush=True)
        time.sleep(0.03)
    print("\n")

def main():
    """メイン実行関数"""
    print_episode_intro()
    
    # デバッグ猫を作成
    deba = HungryCat("デバッグ")
    
    print("デバの最初の出勤日が始まります...")
    print()
    
    # シミュレーション: 1日の開発作業
    for session in range(3):
        print(f"\n--- セッション {session + 1} ---")
        deba.debug_session()
        time.sleep(1)
    
    # 日次サマリー
    print("\n" + "=" * 30)
    print("📊 今日の成果")
    print("=" * 30)
    print(f"発見したバグ数: {deba.bugs_found}")
    print(f"最終お腹レベル: {deba.hunger_level}/10")
    print(f"最終エネルギー: {deba.energy_level}/10")
    
    if deba.bugs_found > 0:
        print("\n🎉 初日から活躍できたニャン！")
        print("明日はもっと頑張るニャ〜")
    else:
        print("\n😸 明日はきっともっとバグを見つけるニャン！")
    
    print("\n次回：第2話「バグとマグロ」をお楽しみに！")

if __name__ == "__main__":
    main()