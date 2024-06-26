import requests
import json

# APIキーを取得
config = json.load(open('config.json'))

def get_top_headlines(api_key , country = 'jp' , category = 'general' , page_size = 5):
    base_url = 'https://newsapi.org/v2/top-headlines'
    headers = {'X-Api-Key': api_key}
    params = {
        'country': country,
        'category': category,
        'pageSize': page_size
    }

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    if data['status'] == 'ok':
        return data['articles']
    else:
        return None
    


def post_to_discord(webhook_url, news, include_title=True):
    for article in news:
        try:
            if include_title:
                message_content = f"**{article['title']}**\n{article['description']}\nRead more: {article['url']}"
            else:
                message_content = f"{article['description']}\nRead more: {article['url']}"

            payload = {
                'content': message_content
            }

            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()  # レスポンスがエラーでないことを確認

            # レスポンスのステータスコードが204以外の場合、エラーメッセージを表示
            if response.status_code != 204:
                print(f"Failed to post news: Status code {response.status_code}")
            else:
                print(f"Successfully posted news: {article['title']}")

        except requests.exceptions.RequestException as e:
            # リクエストが失敗した場合のエラーメッセージを表示
            print(f"Error posting news: {e}")

        except Exception as e:
            # その他の予期せぬエラーが発生した場合のエラーメッセージを表示
            print(f"Unexpected error: {e}")


def is_webhook_valid(webhook_url):
    test_message = "This is a test message."

    payload = {
        'content': test_message
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 204:
        return True  # 成功ステータスコード
    else:
        return False

def main():
    # DiscordのWebhook URLを読み込む
    webhook_url = config['webhook']
    
    # DiscordのWebhookのURL
    if not is_webhook_valid(webhook_url):
        print("Invalid Discord webhook URL.")
        return

    # News APIのAPIキーを読み込
    api_key = config['api_key']

    # トップニュースを取得
    news = get_top_headlines(api_key, country='jp', category='general')

    if news:
        # Discordにニュースを投稿
        post_to_discord(webhook_url, news)
    else:
        print("Failed to get top headlines.")

if __name__ == "__main__":
    main()
