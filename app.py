import os
import json
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ChatGPT API服務地址和API密鑰
chatgpt_api_url = os.getenv('CHATGPT_API_URL')
chatgpt_api_key = os.getenv('CHATGPT_API_KEY')

# LINE Messaging API SDK相關設置
line_bot_api = LineBotApi('YABdytWjFKQkr6K5SVvkSnWiXzHqSz7v/EOgjSzYY7D3AVfmi/BnffWd+TJ//57nuUPSSmBO/ih/Y5u1vdgc5BCj2YKt37Z6hYTaGkY5OoJ5ed+QIoE8brcwi+3tVEtyWiPgNClNIGlGtI9alkqYsQdB04t89/1O/w1cDnyilFU=
')
handler = WebhookHandler('4cfa733508ecea8d9a8ee71e366ef0d8')

# 定義Flask應用程式實例
app = Flask(__name__)

# 定義處理用戶輸入的函數
def process_message(user_message):
    headers = {'Authorization': 'Bearer ' + chatgpt_api_key}
    payload = {'input': user_message}
    response = requests.post(chatgpt_api_url, headers=headers, data=json.dumps(payload))
    chatgpt_output = json.loads(response.content)
    bot_response = chatgpt_output['response']
    print(user_message)
    print(response)
    print(chatgpt_output)
    print(bot_response)
    return bot_response

# 定義LINE的Webhook事件處理函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 獲取用戶發送的消息
    user_message = event.message.text
    # 使用ChatGPT API生成機器人回復
    bot_response = process_message(user_message)
    # 將回復發送給用戶
    reply_message = TextSendMessage(text=bot_response)
    line_bot_api.reply_message(event.reply_token, reply_message)

    # 輸出除錯訊息
    print(user_message)
    print(bot_response)
    print(reply_message)

# 定義LINE機器人的Webhook路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:   
      handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'

# 使用LINE機器人
if name == "main":
app.run()                          
                         
                          
                       

