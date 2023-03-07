import os
import json
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 定義 LINE Bot API 相關設定
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 定義 ChatGPT API 相關設定
chatgpt_api_url = os.getenv('CHATGPT_API_URL', default='https://api.chatgpt.com/v1/chat')
chatgpt_api_key = os.getenv('CHATGPT_API_KEY')

# 定義 Flask 應用程式實例
app = Flask(__name__)

# 定義處理用戶輸入的函數
def process_message(user_message):
    headers = {'Authorization': 'Bearer ' + chatgpt_api_key}
    payload = {'input': user_message}
    response = requests.post(chatgpt_api_url, headers=headers, data=json.dumps(payload))
    chatgpt_output = json.loads(response.content)
    bot_response = chatgpt_output['response']
    return bot_response

# 定義 LINE 的 Webhook 事件處理函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 獲取用戶發送的消息
    user_message = event.message.text
    # 使用 ChatGPT API 生成機器人回復
    bot_response = process_message(user_message)
    # 將回復發送給用戶
    reply_message = TextSendMessage(text=bot_response)
    line_bot_api.reply_message(event.reply_token, reply_message)

# 定義 LINE Bot 的 Webhook 路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 啟動 LINE Bot
if __name__ == "__main__":
    app.run()
