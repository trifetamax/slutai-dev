import os
import json
from pathlib import Path
from typing import List
from transformers import pipeline

# 環境変数を読み込む
from dotenv import load_dotenv

load_dotenv()

# データファイルのパスと出力ファイルのパス
DATA_FILE = "coin_data.json"  # コインデータを含むJSONファイル
OUTPUT_FILE = "generated_tweets.txt"  # 生成されたツイートを保存するファイル

def load_coin_data(file_path: str) -> dict:
    """コインデータをJSONファイルから読み込む"""
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"{file_path} が存在しません。")
    with open(file_path, "r") as file:
        return json.load(file)

def generate_tweets(coin_data: dict, model_name: str = "gpt2") -> List[str]:
    """ローカルLLMモデルを使用してツイートを生成する"""
    generator = pipeline("text-generation", model=model_name)
    
    coin_name = coin_data.get("name", "Unknown Coin")
    ticker = coin_data.get("ticker", "UNKNOWN")
    description = coin_data.get("description", "")
    
    prompts = [
        f"Create a promotional tweet about {coin_name} ({ticker}).",
        f"Why should you invest in {coin_name}? Here's why:",
        f"Learn about {coin_name}, the future of cryptocurrency: {description}",
    ]
    
    tweets = []
    for prompt in prompts:
        print(f"プロンプト: {prompt}")
        generated = generator(prompt, max_length=280, num_return_sequences=1)
        tweets.append(generated[0]["generated_text"])
    
    return tweets

def save_tweets(tweets: List[str], file_path: str):
    """生成されたツイートをテキストファイルに保存する"""
    with open(file_path, "w") as file:
        for tweet in tweets:
            file.write(tweet + "\n\n")
    print(f"ツイートが {file_path} に保存されました。")

def main():
    """メインスクリプト"""
    try:
        # コインデータを読み込む
        print("コインデータを読み込んでいます...")
        coin_data = load_coin_data(DATA_FILE)
        
        # ツイートを生成する
        print("ツイートを生成中...")
        tweets = generate_tweets(coin_data)
        
        # ツイートを保存する
        print("ツイートを保存中...")
        save_tweets(tweets, OUTPUT_FILE)
        
        print("処理が完了しました！")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
