#偵測有無物體靠近 -> 若有則打開相機 -> 拍照存檔 -> 放入模型比較 -> 回傳結果打開門

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import datetime
from flask import Flask, request, abort, make_response
from random import randint
import RPi.GPIO as GPIO
#import RPi.GPIO as gpio
from picamera import PiCamera
import threading
import time
import numpy as np
from tflite_runtime.interpreter import Interpreter
import cv2
from lite_lib import load_labels, set_input_tensor, classify_image

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
IR_PIN = 36
GPIO.setup(IR_PIN, GPIO.IN)
led1 = 13
led2 = 11
led3 = 15
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
#GPIO.cleanup()
#IR_PIN = 36
#led = 11

@app.route("/check")
def hello():
    return "checked"


# http://127.0.0.1:5000/set?name=dog_name&time=1/3/12:20-13:20
@app.route("/set", methods=['GET'])
def getname():
    name = request.args.get('name')
    total_time = request.args.get('time')
    print(name, total_time)
    alert_door1_door2(total_time)
    return "set_finished"


def alert_door1_door2(set_time):
    date_list = set_time.split('/')
    time_list = date_list[2].split('-')
    now_time = datetime.datetime.now()
    print(now_time)
    next_year = now_time.year
    next_month = date_list[0]
    next_day = date_list[1]
    time1 = time_list[0] + ':00'
    time2 = time_list[1] + ':00'
    print(time1)
    next_time1 = datetime.datetime.strptime(str(next_year) + '-' + str(next_month) + '-' + str(next_day) + ' ' + str(time1), "%Y-%m-%d %H:%M:%S")
    next_time2 = datetime.datetime.strptime(str(next_year) + '-' + str(next_month) + '-' + str(next_day) + ' ' + str(time2), "%Y-%m-%d %H:%M:%S")
    door1_time = (next_time1 - now_time).total_seconds()
    door2_time = (next_time2 - now_time).total_seconds()
    print(door1_time)
    timer = threading.Timer(door1_time, auto_photo())
    timer.start()

    timer2 = threading.Timer(door2_time, door3_close())
    timer2.start()


# http://127.0.0.1:5000/door1?status=start
@app.route("/door1", methods=['GET'])
def start_door1():
    status = request.args.get('status')
    print(status)
    if status == 'start':
        auto_photo()
    return "start_door1_function"


# http://127.0.0.1:5000/door2?status=start
@app.route("/door2", methods=['GET'])
def start_door2():
    status = request.args.get('status')
    print(status)
    if status == 'start':
        door3_close()
    return "start_door2_function"


@app.route('/picamera', methods=['GET'])
def send_image():
    camera = PiCamera()
    camera.capture('dog.jpg')
    camera.close()
    image_data = open('dog.jpg', 'rb').read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response


#拍照部分

def auto_photo():
    #GPIO.setup(IR_PIN, GPIO.IN)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(13, GPIO.LOW)
    print('start detection')
    detected = False

    while True:
        try:
            if GPIO.input(IR_PIN) == GPIO.HIGH and not detected:
                detected = True
                print('detected object')
                random_num = randint(0, sys.maxsize)
                camera = PiCamera()
                camera.resolution(224, 224)
                camera.start_preview()
                camera.capture('./image.jpg')
                camera.stop_preview()
                camera.close()
                print('photo taken')
                #放入模型比較

                #test model
                label_path = 'model/set2_labels.txt'
                model_path = 'model/set2_model.tflite'
                img_name = 'image.jpg'
                test(label_path, model_path, img_name)
                print(labels[label_id])
                #print('test finished')
                #test model
                #if format(labels[label_id]) == '3 cat':
                    #print("a cat")
                #else:
                    #print("not a cat")
            elif GPIO.input(IR_PIN) == GPIO.LOW:
                detected = False
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            GPIO.cleanup()
            exit()
    #except Exception as e:
        #print(e)

def test(label_path, model_path, img_name):
    labels = load_labels(label_path)
    interpreter = Interpreter(model_path)
    print("Model Loaded Successfully.")

    interpreter.allocate_tensors()
    _, height, width, channel = interpreter.get_input_details()[0]['shape']
    print("Required input Shape ({}, {}, {})".format(height, width, channel))

    # load image for inference & preprocessing.
    # the data are normalized to 0~1 whrn training,
    # remenber to do it when inference
    image_show = cv2.imread(img_name)
    image = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (width, height))
    image = image / 255.0  # <- change the pixel range from 0~255 to 0~1

    # run inference on input image & measure the time spent
    results = classify_image(interpreter, image)  # inference first time
    start_time = time.time()
    results = classify_image(interpreter, image)  # inference second time
    stop_time = time.time()
    label_id, prob = results[0]

    # print predict result~
    print(50 * "=")
    print("Object in {} is a/an...".format(img_name))
    print("{}! Confidence={}".format(labels[label_id], prob))
    print(50 * "=")
    print("Time spend: {:.5f} sec.".format(stop_time - start_time))
    cv2.imshow('img', image_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if labels[label_id] == '1 Mimi_cat2':
        print('True')
        blub()
    else:
        print('False')
        GPIO.output(11, GPIO.LOW)
        auto_photo()

    # show image
    #cv2.imshow('img', image_show)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

#gpio.setmode(gpio.BCM)
def blub():
    print('blub function')
    wait_time = 0.2
    #led = 11
    GPIO.setup(led2, GPIO.OUT)

    pre_status = None
    pre_time = time.time()
    current_time = None
    cnt = 0
    print('blub light')
    GPIO.output(11, GPIO.HIGH)
    auto_photo()

def door3_close():
    GPIO.output(15, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(15, GPIO.LOW)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    #GPIO.cleanup()
    app.run(host='0.0.0.0')
