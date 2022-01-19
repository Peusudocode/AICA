# -*- coding: utf-8 -*-

from time import sleep
from flask import Flask, make_response

## comment this line if not execute on RPi
from picamera import PiCamera

# initialize a Flask object
app = Flask(__name__)


@app.route('/picamera', methods=['GET'])
def picamera_image():
    ## comment these lines if not execute on RPi
    camera = PiCamera()
    camera.start_preview()
    camera.capture('./image.jpg')
    camera.stop_preview()
    camera.close()
    image_data = open('./image.jpg', 'rb').read()

    ## comment this line when execute on RPi
    # image_data = open('./Flask.png', 'rb').read()

    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)
