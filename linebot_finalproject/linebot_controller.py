# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import configparser
import linebot_function as lf


# pip3 install line-bot-sdk, flask
app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

    text = event.message.text
    print(text[0:2])
    # 註冊
    if text == '註冊':
        response = lf.enrollment_make_directory(event.source.user_id)
    # 名字:小白、小黃
    elif text[0:2] == '名字':
        response = lf.make_dog_name_directory(event.source.user_id, text)
    # 訂食:小白-1/3/12:00-13:00
    elif text[0:2] == '訂時':
        print("定時")
        input_text = text[3:]
        response = lf.set_feeding_time(event.source.user_id, input_text)
    # 查看:小白
    elif text[0:2] == '查看':
        input_text = text[3:]
        response, status = lf.take_picture(event.source.user_id, input_text)
        print(response, status)
        if status == 'success':
            line_bot_api.push_message(event.source.user_id, ImageSendMessage(original_content_url=response,preview_image_url=response))
            response = input_text + 'picture'

    line_bot_api.push_message(event.source.user_id,TextSendMessage(text=response))


if __name__ == "__main__":
    app.run()