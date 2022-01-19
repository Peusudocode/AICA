# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from random import randint
import json
import threading
import configparser

import RPi.GPIO as GPIO
from picamera import PiCamera
from flask import Flask, request, abort, make_response
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

# initialize a Flask object
app = Flask(__name__)

# get config values from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# initialize objects related to line-bot-sdk
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'), timeout=3000)
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# pre-defined JSON file path of user_id list
# will be create automatically if the file is not exist or the data structure is not a list
USER_LIST_FILE = './user.json'


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


@app.route('/picamera/<counter>', methods=['GET'])
def picamera_image(counter):

    while True:
        try:
            camera = PiCamera()
            camera.start_preview()
            camera.capture('./image.jpg')
            camera.stop_preview()
            camera.close()
            break
        except Exception as e:
            print(e)


    image_data = open('./image.jpg', 'rb').read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'

    return response


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # enroll as a user
    if event.message.text == '即時影像':
        print('got a \"即時影像\" message')

        # append current user id into user_list file
        with open(USER_LIST_FILE, 'r', encoding='utf-8') as file:
            user_list = json.load(file)
        user_list.append(event.source.user_id)
        user_list = list(set(user_list))
        with open(USER_LIST_FILE, 'w', encoding='utf-8') as file:
            json.dump(user_list, file, ensure_ascii=False, indent=4)
        auto_photo()
        # reply success message
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='success'))


def auto_photo():
    print('take picture')

    while True:
        try:
            random_num = randint(0, sys.maxsize)

            with open(USER_LIST_FILE, 'r', encoding='utf-8') as file:
                user_list = json.load(file)
            for user_id in user_list:
                line_bot_api.push_message(user_id,
                                          ImageSendMessage(
                                              original_content_url=config.get('ngrok',
                                                                              'server_name') + '/picamera/{}'.format(
                                                  str(random_num)),
                                              preview_image_url=config.get('ngrok',
                                                                           'server_name') + '/picamera/{}'.format(
                                                  str(random_num))
                                          )
                                          )
            break
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            GPIO.cleanup()
            exit()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        with open(USER_LIST_FILE, 'r', encoding='utf-8') as file:
            user_list = json.load(file)
        if type(user_list) != list:
            raise TypeError()
    except:
        with open(USER_LIST_FILE, 'w', encoding='utf-8') as file:
            json.dump(list(), file, ensure_ascii=False, indent=4)
    finally:
        app.run(debug=False, port=5000)
