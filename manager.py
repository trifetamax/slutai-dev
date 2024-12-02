import os
import requests
import json
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

PUMP_FUN_API_URL = "https://api.pump.fun"  # Pump.funのAPIベースURL
API_KEY = os.getenv("PUMP_FUN_API_KEY")  # Pump.fun APIキー
COIN_TICKER = os.getenv("COIN_TICKER")

# APIキーが設定されていない場合はエラーを発生させる
if not API_KEY:
    raise ValueError("PUMP_FUN_API_KEYが環境変数に設定されていません。")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def update_coin_details(ticker, details):
    """コインの詳細を更新する"""
    print(f"{ticker} の詳細を更新しています...")
    endpoint = f"{PUMP_FUN_API_URL}/coins/{ticker}"
    response = requests.put(endpoint, headers=HEADERS, json=details)
    if response.status_code == 200:
        print(f"{ticker} の詳細が更新されました。")
        return response.json()
    else:
        print(f"エラー: {response.status_code} - {response.text}")
        return None

def fetch_coin_stats(ticker):
    """コインの統計情報を取得する"""
    print(f"{ticker} の統計情報を取得しています...")
    endpoint = f"{PUMP_FUN_API_URL}/coins/{ticker}/stats"
    response = requests.get(endpoint, headers=HEADERS)
    if response.status_code == 200:
        stats = response.json()
        print(f"{ticker} の統計情報: {stats}")
        return stats
    else:
        print(f"エラー: {response.status_code} - {response.text}")
        return None

def promote_coin(ticker):
    """コインをプロモートする"""
    print(f"{ticker} をプロモートしています...")
    endpoint = f"{PUMP_FUN_API_URL}/coins/{ticker}/promote"
    response = requests.post(endpoint, headers=HEADERS)
    if response.status_code == 200:
        print(f"{ticker} のプロモーションが成功しました。")
        return response.json()
    else:
        print(f"エラー: {response.status_code} - {response.text}")
        return None

def main():
    """メインスクリプト"""
    try:
        # コインの詳細を更新する例
        new_details = {
            "description": "このコインは未来の金融を変革します。",
            "website": "https://example.com",
            "twitter": "https://twitter.com/example",
        }
        update_response = update_coin_details(COIN_TICKER, new_details)

        # コインの統計情報を取得する例
        stats = fetch_coin_stats(COIN_TICKER)

        # コインをプロモートする例
        promotion_response = promote_coin(COIN_TICKER)

        # 実行結果を保存する
        result = {
            "update_response": update_response,
            "stats": stats,
            "promotion_response": promotion_response,
        }
        with open("coin_management_results.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        print("結果が coin_management_results.json に保存されました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
