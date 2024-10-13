import os
from time import sleep
from dotenv import load_dotenv
import tweepy

# 環境変数を読み込む
load_dotenv()

# Twitter APIの認証情報を環境変数から取得
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# 入力ファイル名
TWEETS_FILE = "generated_tweets.txt"

def authenticate_twitter() -> tweepy.API:
    """Twitter APIに認証する"""
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def read_tweets(file_path: str) -> list:
    """ツイートをファイルから読み込む"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} が見つかりません。")
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

def post_tweets(api: tweepy.API, tweets: list, delay: int = 60):
    """ツイートをTwitterに投稿する"""
    print("ツイートを投稿中...")
    for idx, tweet in enumerate(tweets, start=1):
        try:
            print(f"ツイート {idx}: {tweet}")
            api.update_status(tweet)
            print(f"ツイート {idx} が成功しました。")
            sleep(delay)  # 次のツイートまで待機
        except Exception as e:
            print(f"ツイート {idx} の投稿中にエラーが発生しました: {e}")

def main():
    """メインスクリプト"""
    try:
        # API認証
        print("Twitter APIに認証中...")
        api = authenticate_twitter()
        
        # ツイートを読み込む
        print("ツイートをファイルから読み込んでいます...")
        tweets = read_tweets(TWEETS_FILE)
        
        # ツイートを投稿する
        if tweets:
            print(f"{len(tweets)}件のツイートを投稿します...")
            post_tweets(api, tweets)
        else:
            print("投稿するツイートがありません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
