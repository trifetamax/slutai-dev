import os
import json
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from steel import Steel

# .envファイルから環境変数を読み込む
load_dotenv()

COIN_NAME = os.getenv('COIN_NAME')
COIN_TICKER = os.getenv('COIN_TICKER')
COIN_DESCRIPTION = os.getenv('COIN_DESCRIPTION')
COIN_IMAGE = os.getenv('COIN_IMAGE')
COIN_WEBSITE = os.getenv('COIN_WEBSITE')
COIN_TWITTER = os.getenv('COIN_TWITTER')
COIN_TELEGRAM = os.getenv('COIN_TELEGRAM')

STEEL_API_KEY = os.getenv('STEEL_API_KEY')

# 環境変数でSTEEL_API_KEYが設定されていない場合はエラーを発生させる
if not STEEL_API_KEY:
    raise ValueError("STEEL_API_KEYが環境変数に設定されていません。")

# 環境変数からSteelクライアントを初期化する
client = Steel(
    steel_api_key=STEEL_API_KEY,
)

def save_to_file(data, filename="output.json"):
    """抽出したデータをJSONファイルに保存する"""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"データが{filename}に保存されました")

def capture_screenshot(page, filename="screenshot.png"):
    """現在のページのスクリーンショットをキャプチャする"""
    page.screenshot(path=filename, full_page=True)
    print(f"スクリーンショットが{filename}として保存されました")

def log_error(error_message):
    """エラーメッセージをファイルに記録する"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {error_message}\n")

def main():
    session = None
    browser = None

    try:
        print("Steelセッションを作成中...")

        # 新しいSteelセッションを作成する
        session = client.sessions.create()

        print(f"""セッションが正常に作成されました。セッションID: {session.id}
以下のURLでライブビューが確認できます: {session.session_viewer_url}
        """)

        # PlaywrightをSteelセッションに接続する
        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(
            f"wss://connect.steel.dev?apiKey={STEEL_API_KEY}&sessionId={session.id}"
        )

        print("Playwrightを介してブラウザに接続しました")

        # 新しいページを作成する
        page = browser.new_page()

        # Pump.funの「コイン作成」ページに移動する
        print("Pump.funのコイン作成ページに移動中...")
        page.goto("https://pump.fun/create", wait_until="networkidle")

        # ページのスクリーンショットを撮る
        capture_screenshot(page, filename="pump.png")

        # フォームを入力する
        print("フォームに入力中...")
        page.fill("input[name=name]", COIN_NAME)
        page.fill("input[name=ticker]", COIN_TICKER)
        page.fill("textarea[name=description]", COIN_DESCRIPTION)
        
        # 画像をアップロードする
        print("画像をアップロード中...")
        page.set_input_files("input[name=image]", files=[COIN_IMAGE])
        
        # ソーシャルリンクを設定する
        print("ソーシャルリンクを設定中...")
        page.fill("input[name=website]", COIN_WEBSITE)
        page.fill("input[name=twitter]", COIN_TWITTER)
        page.fill("input[name=telegram]", COIN_TELEGRAM)

        # フォームを送信する
        print("フォームを送信中...")
        page.click("text=create coin")

        # 1 SOLを支払う
        print("1 SOLを支払っています...")
        page.fill("input[name=amount]", "1")
        page.click("text=create coin")

        # トランザクションハッシュを取得する
        transaction_hash = page.locator("text=Transaction hash").locator("xpath=following-sibling::div").text_content()
        print(f"トランザクションハッシュ: {transaction_hash}")

        # トランザクションハッシュをファイルに保存する
        save_to_file({"transaction_hash": transaction_hash}, filename="transaction.json")

    except Exception as e:
        error_message = f"エラーが発生しました: {e}"
        print(error_message)
        log_error(error_message)

    finally:
        # 最終処理: ブラウザを閉じ、セッションを解放する
        if browser:
            browser.close()
            print("ブラウザを閉じました")

        if session:
            print("セッションを解放中...")
            client.sessions.release(session.id)
            print("セッションが解放されました")

        print("完了！")

# スクリプトを実行する
if __name__ == "__main__":
    main()
