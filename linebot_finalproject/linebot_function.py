# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import requests
import datetime
import threading
# pip install requests


def enrollment_make_directory(userid):
    folder = os.path.exists(userid)
    if not folder:
        # 如果不存在，則建立新目錄
        os.makedirs(userid)
        text = '註冊成功，請輸入您所有寵物的名字，格式如名字:小白、小黃'
        return text
    else:
        text = '您已註冊，可改用修改註冊'
        return text


def make_dog_name_directory(userid, dog_name_text):
    print(dog_name_text)
    folder = os.path.exists(userid)
    if not folder:
        text = '您還沒註冊請先註冊'
        return text
    else:
        dog_dictionary = {'name': 'raspberrypi_url'}
        dog_name_list = dog_name_text.split('：')[1].split('、')
        dog_amount = len(dog_name_list)
        print(dog_name_list, dog_amount)
        for x in range(dog_amount):
            folder_path = userid + '\\' + str(x)
            os.makedirs(folder_path)
            dog_dictionary[dog_name_list[x]] = 'empty'
        filename = userid + '.json'
        file = open(filename, "w", encoding='utf-8')
        json.dump(dog_dictionary, file)
        file.close()
        text = '註冊成功'
        return text


def set_feeding_time(userid, set_text):
    folder = os.path.exists(userid)
    filename = userid + '.json'
    if not folder:
        text = '您還沒註冊請先註冊'
        return text
    else:
        feeding_list = set_text.split('、')
        feeding_length = len(feeding_list)
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for x in range(feeding_length):
                name = feeding_list[x].split('-')[0]
                time1 = feeding_list[x].split('-')[1]
                time2 = feeding_list[x].split('-')[2]
                raspberrypi = data.get(name)
                if raspberrypi == 'empty':
                    text = '尚未設定raspberry pi'
                    status = 'fail'
                    break
                else:
                    url = raspberrypi
                    print(time1, time2, url)
                    response = alert_door1_door2(time1, url, time2)
                    text = "設定成功"
        return text


def send_door1_start(url):
    print(url)
    door1_url = url + '/door1?status=start'
    print(door1_url)
    response = requests.get(door1_url)
    print(response)


def send_door2_start(url):
    print(url)
    door2_url = url + '/door2?status=start'
    print(door2_url)
    response = requests.get(door2_url)
    print(response)


def take_picture(userid, picture_text):
    print(picture_text)
    folder = os.path.exists(userid)
    if not folder:
        text = '您還沒註冊請先註冊'
        status = 'fail'
        return text, status
    else:
        name = picture_text
        print(name)
        filename = userid + '.json'
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            raspberrypi = data.get(name)
            print(raspberrypi)
            if raspberrypi == 'empty':
                text = '尚未設定raspberry pi'
                status = 'fail'
            else:
                text = raspberrypi + '/picamera'
                status = 'success'
        return text, status


def alert_door1_door2(set_time, url, end_time):
    print(set_time, end_time)
    print(url)
    date_list = set_time.split('/')
    now_time = datetime.datetime.now()
    next_year = now_time.year
    next_month = date_list[0]
    next_day = date_list[1]
    time1 = date_list[2] + ':00'
    time2 = end_time + ':00'
    next_time1 = datetime.datetime.strptime(str(next_year) + '-' + str(next_month) + '-' + str(next_day) + ' ' + str(time1), "%Y-%m-%d %H:%M:%S")
    next_time2 = datetime.datetime.strptime(str(next_year) + '-' + str(next_month) + '-' + str(next_day) + ' ' + str(time2), "%Y-%m-%d %H:%M:%S")
    door1_time = (next_time1 - now_time).total_seconds()
    door2_time = (next_time2 - now_time).total_seconds()

    timer1 = threading.Timer(door1_time, send_door1_start, (url,))
    timer1.start()
    timer2 = threading.Timer(door2_time, send_door2_start, (url,))
    timer2.start()
    return "set_finished"

