import time
import RPi.GPIO as GPIO
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
Button_PIN = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Button_PIN, GPIO.IN)
camera = PiCamera()
camera.resolution = (320, 240)

def change_image_style(date):
    month = date.split("-")[1]
    day = date.split("-")[2].split()[0]
    hour = date.split()[1].split(":")[0]
    minute = date.split(":")[1]
    output = month + day + "_" + hour + minute + ".jpg"
    net = cv2.dnn.readNetFromTorch('model/starry_night.t7') # 讀取風格檔，這裡讀入「星空」的風格
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    img = cv2.imread("image.jpg")
    (h, w) = img.shape[:2]
    # 把影像修改成神經網路可以使用的格式
    blob = cv2.dnn.blobFromImage(img, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
    net.setInput(blob)  # 把影像丟入模型做風格轉換
    out = net.forward() # 開始轉換
    out = out.reshape(3, out.shape[2], out.shape[3])
    out[0] += 103.939
    out[1] += 116.779
    out[2] += 123.68
    # out /= 255
    out = out.transpose(1, 2, 0)
    cv2.imwrite(output, out)
    img = cv2.imread(output)
    cv2.imshow("change", img)  # 將 img 輸出至視窗
    cv2.waitKey(100)

try:
    while True:
        if GPIO.input(Button_PIN) == GPIO.HIGH:
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(date)
            camera.capture("image.jpg")
            change_image_style(date)
except KeyboardInterrupt:
    print('interrupt')
finally:
    GPIO.cleanup()
    camera.close()
    cv2.destroyAllWindows()

