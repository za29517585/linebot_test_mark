import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# ---------------------------------------------------
# 設定區
# 如果您還在本地測試，請直接填入字串
# 如果已部署到 Render，請保留 os.getenv 寫法
# ---------------------------------------------------
# 本地測試時，請將 os.getenv(...) 換成您的真實 Token 字串，例如： '你的ChannelAccessToken'
# CHANNEL_ACCESS_TOKEN = '你的 Channel Access Token'
# CHANNEL_SECRET = '你的 Channel Secret'

# 為了方便您現在除錯，若沒有設定環境變數，這裡先用空字串避免報錯 (請記得填入)
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 表頭
    signature = request.headers['X-Line-Signature']

    # 取得請求內容 (body)
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# ---------------------------------------------------
# 修正後的事件處理器
# ---------------------------------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 這裡實作回聲功能：用戶傳什麼，就回傳什麼
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    app.run(port=5000)