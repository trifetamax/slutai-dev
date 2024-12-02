import tweepy
import os
import json
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# Twitter APIの認証情報を環境変数から取得
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# 保存するファイル名
OUTPUT_FILE = "replies_and_dms.json"

def authenticate_twitter() -> tweepy.API:
    """Twitter APIに認証する"""
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def fetch_replies(api: tweepy.API, user_screen_name: str) -> list:
    """リプライを取得する"""
    print(f"@{user_screen_name}宛てのリプライを取得中...")
    replies = []
    for tweet in tweepy.Cursor(api.search_tweets, q=f"@{user_screen_name}", tweet_mode="extended").items(50):
        if hasattr(tweet, "in_reply_to_screen_name") and tweet.in_reply_to_screen_name == user_screen_name:
            replies.append({
                "id": tweet.id,
                "user": tweet.user.screen_name,
                "text": tweet.full_text,
                "created_at": tweet.created_at.isoformat(),
            })
    return replies

def fetch_dms(api: tweepy.API) -> list:
    """ダイレクトメッセージを取得する"""
    print("ダイレクトメッセージを取得中...")
    dms = []
    for dm in api.get_direct_messages(count=50):
        dms.append({
            "id": dm.id,
            "sender": dm.message_create["sender_id"],
            "text": dm.message_create["message_data"]["text"],
            "created_at": dm.created_timestamp,
        })
    return dms

def save_to_file(data: dict, file_path: str):
    """取得したデータをファイルに保存する"""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"データが {file_path} に保存されました。")

def main():
    """メインスクリプト"""
    try:
        # API認証
        print("Twitter APIに認証中...")
        api = authenticate_twitter()
        
        # ユーザー名を取得する
        user_screen_name = api.verify_credentials().screen_name
        
        # リプライを取得する
        replies = fetch_replies(api, user_screen_name)
        
        # ダイレクトメッセージを取得する
        dms = fetch_dms(api)
        
        # 取得したデータをまとめる
        data = {
            "replies": replies,
            "dms": dms,
        }
        
        # データをファイルに保存する
        save_to_file(data, OUTPUT_FILE)
        
        print("処理が完了しました！")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
